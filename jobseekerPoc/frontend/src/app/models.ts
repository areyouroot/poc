export interface Config {
  maps_api_key: string;
  search_api_key: string;
  search_cx: string;
  llm_provider: string;
  llm_base_url?: string;
  llm_api_key?: string;
}

export interface SearchRequest {
  latitude: number;
  longitude: number;
  radius_km: number;
  sectors: string[];
}

export interface Company {
  name: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  place_id?: string;
  rating?: number;
  types: string[];
}

export interface IntelligenceData {
  is_hiring: boolean;
  job_sources: string[];
  emails: string[];
  summary?: string;
}
