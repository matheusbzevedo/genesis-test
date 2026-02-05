from rest_framework import viewsets

from .models import Gene
from .serializers import GeneSerializer


class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset
