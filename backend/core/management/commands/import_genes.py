import requests
from django.core.management.base import BaseCommand

from core.models import Gene


class Command(BaseCommand):
    help = "Import genes data from OMIM and HGNC"

    def handle(self, *args, **options):
        # download JSON
        url_hgnc = (
            "https://www.genenames.org/cgi-bin/genegroup/download-all?format=json"
        )
        self.stdout.write(f"Downloading HGNC: {url_hgnc}")

        try:
            response = requests.get(url_hgnc, timeout=60)
            response.raise_for_status()
            genes_list = response.json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error HGNC: {e}"))
            return

        hgnc_map = {}

        for item in genes_list:
            ncbi_id = item.get("ncbiGeneID")

            if ncbi_id:
                hgnc_map[str(ncbi_id)] = {
                    "symbol": item.get("approvedSymbol"),
                    "name": item.get("approvedName"),
                }

        self.stdout.write(f"HGNC processing: {len(hgnc_map)} genes indexed.")

        # download txt
        url_omim = "https://www.omim.org/static/omim/data/mim2gene.txt"
        self.stdout.write(f"Downloading OMIM: {url_omim}")

        try:
            response = requests.get(url_omim, stream=True, timeout=60)
            response.raise_for_status()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error OMIM: {e}"))
            return

        genes_to_create = []
        existing_ids = set()

        lines = response.iter_lines(decode_unicode=True)

        for line in lines:
            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) < 3:
                continue

            mim_number = parts[0].strip()
            entrez_id = parts[2].strip()

            if entrez_id and entrez_id in hgnc_map:
                # avoid duplicates
                if entrez_id in existing_ids:
                    continue

                hgnc_data = hgnc_map[entrez_id]

                genes_to_create.append(
                    Gene(
                        entrez_gene_id=int(entrez_id),
                        mim_number=int(mim_number),
                        symbol=hgnc_data["symbol"],
                        approved_name=hgnc_data["name"],
                    )
                )
                existing_ids.add(entrez_id)

        if not genes_to_create:
            self.stdout.write(
                self.style.WARNING("No gene found. Verify if the ids match")
            )
            return

        self.stdout.write("Cleaning old data")
        Gene.objects.all().delete()

        self.stdout.write(f"Saving {len(genes_to_create)} genes...")
        Gene.objects.bulk_create(genes_to_create, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(f"SUCCESS {len(genes_to_create)} genes imported!")
        )
