from rest_framework import viewsets
from .models import Gene
from .serializers import GeneSerializer

class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        min_mim = self.request.query_params.get('min_mim')
        max_mim = self.request.query_params.get('max_mim')

        if min_mim:
            queryset = queryset.filter(mim_number__gte=min_mim)
        if max_mim:
            queryset = queryset.filter(mim_number__lte=max_mim)

        return queryset
