from pydantic import BaseModel
from typing import List, Optional

class Config(BaseModel):
    maps_api_key: str
    search_api_key: str
    search_cx: str
    llm_provider: str  # "ollama" or "openai"
    llm_base_url: Optional[str] = None
    llm_api_key: Optional[str] = None

class SearchRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 25.0
    sectors: List[str] = []

class Company(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None
    rating: Optional[float] = None
    types: List[str] = []

class IntelligenceData(BaseModel):
    is_hiring: bool
    job_sources: List[str] = []
    emails: List[str] = []
    summary: Optional[str] = None

class ScanResult(BaseModel):
    company: Company
    intelligence: IntelligenceData
