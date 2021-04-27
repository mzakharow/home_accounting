import datetime
from collections import OrderedDict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from rest.serializers import TransferSerializer
from transfers.models import Transfer, CategoryTransfer


class TransferApiTestCase(APITestCase):
    def test_get(self):
        category = CategoryTransfer.objects.create(name='category test 1')
        user = User.objects.create(username='test_user_1')
        transfer_1 = Transfer.objects.create(user=user, data=datetime.datetime.now(), sum=109.98, category=category, comment='test 1', type_transfer='1')
        url = reverse('transfer-list')
        print(url)
        response = self.client.get(url)
        serializer_data = TransferSerializer(transfer_1).data
        # self.assertEqual(TransferSerializer([transfer_1, transfer_=2], many=True).data)
        self.assertEqual(serializer_data, response.data)

