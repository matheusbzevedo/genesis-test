from django.db import models

class Gene(models.Model):
    entrez_gene_id = models.BigIntegerField(unique=True, db_index=True)
    mim_number = models.IntegerField(null=True, blank=True, db_index=True)
    symbol = models.CharField(max_length=50)
    approved_name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f"{self.symbol} ({self.entrez_gene_id})"
