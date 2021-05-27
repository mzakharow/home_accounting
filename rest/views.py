from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from rest.permissions import IsOwner
from rest.serializers import TransferSerializer
from transfers.models import Transfer


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwner]
    filter_fields = ['sum', 'user']
    search_fields = ['sum', 'data']
    ordering_fields = ['sum', 'data']

    def get_queryset(self):
        queryset = Transfer.objects.filter(user=self.request.user)
        return queryset
