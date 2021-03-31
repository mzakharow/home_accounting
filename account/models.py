from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """ расширение модели пользователя """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0, verbose_name="Бюджет на месяц")
