
import { HttpClient, HttpParams } from "@angular/common/http";
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

  getGenes(
    page: number = 1,
    pageSize: number = 50,
    minMim?: number,
    maxMim?: number,
  ): Observable<PaginatedResponse<Gene>> {
    let params = new HttpParams().set("offset", page).set("limit", pageSize);

    if (minMim) params = params.set("min_mim", minMim);
    if (maxMim) params = params.set("max_mim", maxMim);

    return this.http.get<PaginatedResponse<Gene>>(this.apiUrl, { params });
  }
}
