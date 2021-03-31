from django.contrib.auth.models import User
from django.db import models


class CategoryTransfer(models.Model):
    """ Модель типа категории проводки """
    DEFAULT_ID = 1
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Transfer(models.Model):
    """ Модель проводки """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='Пользователь')
    data = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    sum = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Сумма")
    category = models.ForeignKey(CategoryTransfer, on_delete=models.SET_DEFAULT, default=CategoryTransfer.DEFAULT_ID, verbose_name='Категория')
    comment = models.CharField(max_length=200, blank=True, verbose_name='Комментарий')
    TYPE_SELECTION = (
        ('+', 'Приход'),
        ('-', 'Расход')
    )
    type_transfer = models.CharField(max_length=1, choices=TYPE_SELECTION, blank=True, default=TYPE_SELECTION[1], verbose_name='Тип движения')

    def __str__(self):
        return f"{self.data.strftime('%m.%d.%y %H:%M:%S')}: {self.type_transfer} {self.sum} руб."
