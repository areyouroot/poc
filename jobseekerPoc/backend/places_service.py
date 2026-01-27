import requests
from typing import List, Optional
from .models import Company

GOOGLE_PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def get_keywords_for_sectors(sectors: List[str]) -> str:
    # A simple mapping helper
    keywords = []
    for sector in sectors:
        s = sector.lower()
        if s == "it" or "software" in s or "tech" in s:
            keywords.append("software company")
            keywords.append("technology")
        elif "hospital" in s or "medical" in s:
            keywords.append("hospital")
            keywords.append("clinic")
        else:
            keywords.append(sector)
    return " OR ".join(keywords) if keywords else "point_of_interest"

def fetch_nearby_companies(lat: float, lon: float, radius_km: float, sectors: List[str], api_key: str) -> List[Company]:
    radius_meters = int(radius_km * 1000)
    keyword = get_keywords_for_sectors(sectors)

    params = {
        "location": f"{lat},{lon}",
        "radius": radius_meters,
        "key": api_key,
        "keyword": keyword
    }

    try:
        response = requests.get(GOOGLE_PLACES_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        companies = []
        if "results" in data:
            for place in data["results"]:
                # Convert Place result to Company model
                loc = place.get("geometry", {}).get("location", {})
                company = Company(
                    name=place.get("name"),
                    address=place.get("vicinity"),
                    latitude=loc.get("lat"),
                    longitude=loc.get("lng"),
                    place_id=place.get("place_id"),
                    rating=place.get("rating"),
                    types=place.get("types", [])
                )
                companies.append(company)

        return companies

    except Exception as e:
        print(f"Error fetching places: {e}")
        return []
