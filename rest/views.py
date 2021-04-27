from rest_framework.viewsets import ModelViewSet

from rest.serializers import TransferSerializer
from transfers.models import Transfer


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
