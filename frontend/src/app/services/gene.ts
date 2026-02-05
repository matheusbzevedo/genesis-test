import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

export interface Gene {
  id: number;
  entrez_gene_id: number;
  mim_number: number;
  symbol: string;
  approved_name: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: "root",
})
export class GeneService {
  private apiUrl = "http://localhost:8000/api/genes/";

  constructor(private http: HttpClient) {}

  getGenes(): Observable<PaginatedResponse<Gene>> {
    return this.http.get<PaginatedResponse<Gene>>(this.apiUrl);
  }
}
