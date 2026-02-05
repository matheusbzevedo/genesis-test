from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase

from core.models import Gene


class ImportGenesCommandTest(TestCase):
    def setUp(self):
        # Fake data for HGNC (JSON)
        self.hgnc_data = [
            {
                "ncbiGeneID": 10554,
                "approvedSymbol": "AGPAT1",
                "approvedName": "1-acylglycerol-3-phosphate",
            },
            {
                "ncbiGeneID": 79888,
                "approvedSymbol": "LPCAT1",
                "approvedName": "lysophosphatidylcholine acyltransferase 1",
            },
        ]

        # Fake data for OMIM (TXT file with tabs)
        # Format: MIM \t Type \t EntrezID \t Symbol \t Ensembl
        self.omim_data = (
            "# Copyright header...\n"
            "100640\tgene\t10554\tAGPAT1\tENSG00000165092\n"  # Match (AGPAT1)
            "100650\tgene\t99999\tUNKNOWN\tENSG00000111275\n"  # No match in HGNC
            "100660\tgene\t79888\tLPCAT1\tENSG00000108602\n"  # Match (LPCAT1)
        )

    @patch("requests.get")
    def test_import_genes_success(self, mock_get):
        """
        Test if the command correctly downloads, merges, and saves genes.
        """
        # HGNC mock
        mock_response_hgnc = MagicMock()
        mock_response_hgnc.json.return_value = self.hgnc_data
        mock_response_hgnc.status_code = 200

        # OMIM mock
        mock_response_omim = MagicMock()
        mock_response_omim.iter_lines.return_value = self.omim_data.splitlines()
        mock_response_omim.status_code = 200

        mock_get.side_effect = [mock_response_hgnc, mock_response_omim]

        out = StringIO()
        call_command("import_genes", stdout=out)

        # Should have created exactly 2 genes (10554 and 79888)
        self.assertEqual(Gene.objects.count(), 2)

        # Verify content of one gene
        gene = Gene.objects.get(entrez_gene_id=10554)
        self.assertEqual(gene.symbol, "AGPAT1")
        self.assertEqual(gene.mim_number, 100640)

        self.assertIn("SUCCESS", out.getvalue())

    @patch("requests.get")
    def test_import_genes_api_failure(self, mock_get):
        """
        Test graceful failure if an API is down.
        """
        # Simulate an exception
        mock_get.side_effect = Exception("Connection Timeout")

        out = StringIO()
        err = StringIO()

        call_command("import_genes", stdout=out, stderr=err)

        self.assertEqual(Gene.objects.count(), 0)

        self.assertIn("Error", err.getvalue())
