from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import Config, SearchRequest, Company, ScanResult, IntelligenceData
from .places_service import fetch_nearby_companies
from .llm_service import analyze_company

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for config (per session ideally, but global for simple local app)
current_config: Config = None

@app.post("/config")
def set_config(config: Config):
    global current_config
    current_config = config
    return {"status": "Config updated"}

@app.get("/config")
def get_config():
    if not current_config:
        raise HTTPException(status_code=404, detail="Config not set")
    return current_config

@app.post("/scan")
def scan_companies(request: SearchRequest) -> List[Company]:
    if not current_config:
        raise HTTPException(status_code=400, detail="Configuration not set. Please configure API keys first.")

    companies = fetch_nearby_companies(
        request.latitude,
        request.longitude,
        request.radius_km,
        request.sectors,
        current_config.maps_api_key
    )
    return companies

@app.post("/analyze")
def analyze_company_endpoint(company: Company, sector: str) -> IntelligenceData:
    if not current_config:
         raise HTTPException(status_code=400, detail="Configuration not set.")

    return analyze_company(company.name, sector, current_config)

@app.get("/health")
def health():
    return {"status": "ok"}
