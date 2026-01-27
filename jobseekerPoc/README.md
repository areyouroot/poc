# JobSeeker POC

A location-based company scanner and intelligence gatherer using Python, Angular, and LLMs.

## Features

- **Location Scanning**: Scans for companies within a given radius using Google Places API.
- **Sector Filtering**: Filter by IT, Hospital, Retail, etc.
- **Intelligence Analysis**:
    - Analyzes each found company using Google Search + LLM (Ollama or OpenAI).
    - Determines if the company is hiring.
    - Finds job listing sources (LinkedIn, Company Careers).
    - Extracts email addresses.
- **Visual Map**: Displays companies on an interactive Google Map.

## Prerequisites

1.  **Python 3.12+**
2.  **Node.js 18+** & **npm**
3.  **Ollama** (optional, for local LLM)
    - Install Ollama from [ollama.com](https://ollama.com).
    - Pull a model: `ollama pull llama3` (or mistral).
4.  **API Keys**:
    - **Google Maps API Key** (with Places API enabled).
    - **Google Custom Search API Key**.
    - **Google Search Engine ID (CX)**.
    - **OpenAI API Key** (optional, if not using Ollama).

## Project Structure

- `backend/`: FastAPI Python application.
- `frontend/`: Angular application.
- `tests/`: End-to-End tests using Playwright.

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Running the Application

You need to run both Backend and Frontend.

### 1. Start Backend

```bash
# From root directory
uvicorn jobseekerPoc.backend.main:app --reload --port 8000
```
The API will run at `http://localhost:8000`.

### 2. Start Frontend

```bash
# From jobseekerPoc/frontend
ng serve
```
The App will run at `http://localhost:4200`.

## Usage

1.  Open `http://localhost:4200` in your browser.
2.  A configuration modal will appear. Enter your API Keys and choose your LLM provider.
    - If using **Ollama**, ensure it is running (`ollama serve`).
3.  Click "Save & Start".
4.  Allow Location Access (or enter manually).
5.  Adjust Radius and Sectors.
6.  Click "Scan Companies".
7.  Watch the map populate and the list below update with hiring status and emails.

## Testing

### Unit Tests (Backend)

```bash
# From root directory
export PYTHONPATH=$PYTHONPATH:$(pwd)/jobseekerPoc
pytest jobseekerPoc/backend/tests
```

### E2E Tests

First, build the frontend:
```bash
cd jobseekerPoc/frontend
ng build
```

Then run the python test script:
```bash
# From root directory
python jobseekerPoc/tests/e2e_test.py
```
This will launch a headless browser, perform a search with mock keys, and save a screenshot to `jobseekerPoc/evidence/`.
