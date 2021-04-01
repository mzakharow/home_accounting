import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from account.models import Profile
from home_accounting import settings
from transfers.models import Transfer


class TestUserOwnerOfTransfer(UserPassesTestMixin):
    """ Миксин, проверяющий совпадение владельца записи с текущим пользователем """
    def test_func(self):
        self.object = self.get_object()
        return self.request.user == self.object.user


@method_decorator(login_required, name='dispatch')
class TransfersView(CreateView):
    """ Создание модели, с расширением в get_context_data вывода списка всех транзакций """
    model = Transfer
    template_name = 'transfers/index.html'
    fields = ('type_transfer', 'sum', 'category', 'comment',)
    success_url = reverse_lazy('transfers-list')

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = self.request.user.transfer_set.all().order_by('-data')
        # time_zone = pytz.timezone(settings.TIME_ZONE)
        time_zone = pytz.timezone('UTC')
        positive_sum = Transfer.objects.filter(user=self.request.user,
                                               type_transfer='+',
                                               data__range=(datetime.datetime.now(time_zone).replace(day=1, hour=0,minute=0,second=0,microsecond=0),
                                                            datetime.datetime.now(time_zone))).aggregate(Sum('sum'))
        negative_sum = Transfer.objects.filter(user=self.request.user,
                                               type_transfer='-',
                                               data__range=(datetime.datetime.now(time_zone).replace(day=1),
                                                            datetime.datetime.now(time_zone))).aggregate(Sum('sum'))
        if positive_sum['sum__sum'] is None:
            positive_sum['sum__sum'] = 0
        if negative_sum['sum__sum'] is None:
            negative_sum['sum__sum'] = 0
        total_sum = positive_sum['sum__sum'] - negative_sum['sum__sum']
        kwargs['total_sum'] = "{:.2f}".format(total_sum)
        kwargs['over_budget'] = Profile.objects.get(user=self.request.user).budget + total_sum
        return super(TransfersView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """ Автоматически подставляет пользователя в запись из запроса """
        form.instance.user = self.request.user
        return super(TransfersView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TransferDetailView(TestUserOwnerOfTransfer, DetailView):
    """ Просмотр записи """
    model = Transfer
    template_name = 'transfers/detail.html'
    context_object_name = 'transfer'


@method_decorator(login_required, name='dispatch')
class TransferUpdateView(TestUserOwnerOfTransfer, UpdateView):
    """ Редактирование записи """
    model = Transfer
    template_name = 'transfers/update.html'
    context_object_name = 'transfer'
    fields = ('type_transfer', 'sum', 'category', 'comment',)

    def get_success_url(self):
        """ путь для перехода при успешном выполнении """
        return reverse_lazy('transfer-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class TransferDeleteView(TestUserOwnerOfTransfer, DeleteView):
    """ Удаление записи """
    model = Transfer
    template_name = 'transfers/delete.html'
    success_url = reverse_lazy('transfers-list')
