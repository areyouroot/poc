import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Config, SearchRequest, Company, IntelligenceData } from '../models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000'; // Hardcoded for POC

  constructor(private http: HttpClient) { }

  setConfig(config: Config): Observable<any> {
    return this.http.post(`${this.apiUrl}/config`, config);
  }

  getConfig(): Observable<Config> {
    return this.http.get<Config>(`${this.apiUrl}/config`);
  }

  scan(request: SearchRequest): Observable<Company[]> {
    return this.http.post<Company[]>(`${this.apiUrl}/scan`, request);
  }

  analyze(company: Company, sector: string): Observable<IntelligenceData> {
    // Send company and sector. The backend expects company object in body and sector as query param?
    // Backend definition:
    // def analyze_company_endpoint(company: Company, sector: str)
    // FastAPI defaults: Pydantic model in body, simple types in query.
    return this.http.post<IntelligenceData>(`${this.apiUrl}/analyze`, company, {
      params: { sector }
    });
  }
}
