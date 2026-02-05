import { CommonModule } from "@angular/common";
import { Component, OnInit, inject, signal } from "@angular/core";
import { FormsModule } from "@angular/forms";

import { MatButtonModule } from "@angular/material/button";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatPaginatorModule } from "@angular/material/paginator";
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MatTableModule } from "@angular/material/table";
import { Gene, GeneService } from "./services/gene";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatPaginatorModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatProgressBarModule,
  ],
  templateUrl: "./app.html",
  styleUrl: "./app.scss",
})
export class App implements OnInit {
  protected readonly tiyle = signal("Frontend");
  private geneService = inject(GeneService);

  displayedColumns: string[] = ["entrez", "mim", "symbol", "name"];
  pageSizeOptions = [10, 25, 50, 100];
  pageSize = signal(10);

  dataSource = signal<Gene[]>([]);
  totalGenes = signal(0);
  pageIndex = signal(0);
  isLoading = signal(false);

  minMim = signal<number | undefined>(undefined);
  maxMim = signal<number | undefined>(undefined);

  ngOnInit() {
    this.loadGenes();
  }

  loadGenes() {
    this.isLoading.set(true);

    this.geneService.getGenes().subscribe({
      next: (response) => {
        this.dataSource.set(response.results);
        this.totalGenes.set(response.count);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error(err);
        this.isLoading.set(false);
      },
    });
  }
}
