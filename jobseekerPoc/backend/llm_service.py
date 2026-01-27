import requests
import json
from typing import List
from .models import IntelligenceData, Config

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

def search_google(query: str, api_key: str, cx: str) -> List[str]:
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": 5  # Top 5 results
    }
    try:
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        snippets = []
        if "items" in data:
            for item in data["items"]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                link = item.get("link", "")
                snippets.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
        return snippets
    except Exception as e:
        print(f"Error searching google: {e}")
        return []

def call_llm(prompt: str, config: Config) -> str:
    if config.llm_provider == "ollama":
        url = f"{config.llm_base_url or 'http://localhost:11434'}/api/generate"
        payload = {
            "model": "llama3", # Default, user might need to change or we make it configurable.
            # I'll assume a default or allow user to pass model in base_url? No.
            # For POC, let's try "llama2" or "mistral" or "llama3". I'll default to "llama3" but fail gracefully?
            # actually better to use the /api/chat if it's chat model.
            # Let's use /api/generate for simplicity with raw prompt.
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        # If user has a different model name, this might fail.
        # I'll add a safe fallback or just use what I have.
        # Actually, let's ask the user to provide model name?
        # For now, I'll hardcode "llama3" but comment.
        try:
            # Try to fetch list of models first? No, too slow.
            # Let's just use 'llama3'.
            payload["model"] = "llama3"
            response = requests.post(url, json=payload)
            if response.status_code == 404: # Model not found maybe?
                 # Fallback to mistral?
                 payload["model"] = "mistral"
                 response = requests.post(url, json=payload)

            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")
            return "{}"

    elif config.llm_provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.llm_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return "{}"
    return "{}"

def analyze_company(company_name: str, sector: str, config: Config) -> IntelligenceData:
    query = f"{company_name} {sector} careers jobs email contact"
    snippets = search_google(query, config.search_api_key, config.search_cx)

    if not snippets:
        return IntelligenceData(is_hiring=False, summary="No search results found.")

    context = "\n\n".join(snippets)

    prompt = f"""
    Analyze the following search results for the company '{company_name}'.
    Determine if they are likely hiring, find any job listing sources (like LinkedIn, Indeed, or company career page), and find any email addresses mentioned.

    Search Results:
    {context}

    Output STRICT JSON format:
    {{
        "is_hiring": boolean,
        "job_sources": [list of strings],
        "emails": [list of strings],
        "summary": "short summary string"
    }}
    """

    json_str = call_llm(prompt, config)

    try:
        # cleanup json string if needed (sometimes LLMs add markdown code blocks)
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
             json_str = json_str.split("```")[1].split("```")[0]

        data = json.loads(json_str)
        return IntelligenceData(
            is_hiring=data.get("is_hiring", False),
            job_sources=data.get("job_sources", []),
            emails=data.get("emails", []),
            summary=data.get("summary", "")
        )
    except Exception as e:
        print(f"Error parsing LLM response: {e}, Response: {json_str}")
        return IntelligenceData(is_hiring=False, summary="Failed to parse intelligence.")
