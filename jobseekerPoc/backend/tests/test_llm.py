from unittest.mock import patch, MagicMock
from backend.llm_service import analyze_company
from backend.models import Config

@patch('backend.llm_service.requests.post')
@patch('backend.llm_service.requests.get')
def test_analyze_company(mock_get, mock_post):
    # Mock Google Search
    mock_search_resp = MagicMock()
    mock_search_resp.status_code = 200
    mock_search_resp.json.return_value = {
        "items": [
            {
                "title": "Careers at Tech Corp",
                "snippet": "We are hiring software engineers! Email us at jobs@techcorp.com",
                "link": "http://techcorp.com/careers"
            }
        ]
    }
    mock_get.return_value = mock_search_resp

    # Mock LLM (Ollama)
    mock_llm_resp = MagicMock()
    mock_llm_resp.status_code = 200
    mock_llm_resp.json.return_value = {
        "response": '{"is_hiring": true, "job_sources": ["Company Site"], "emails": ["jobs@techcorp.com"], "summary": "They are hiring."}'
    }
    mock_post.return_value = mock_llm_resp

    config = Config(
        maps_api_key="map_key",
        search_api_key="search_key",
        search_cx="cx",
        llm_provider="ollama"
    )

    result = analyze_company("Tech Corp", "IT", config)

    assert result.is_hiring is True
    assert "jobs@techcorp.com" in result.emails
    assert "Company Site" in result.job_sources

    mock_get.assert_called_once()
    mock_post.assert_called_once()
