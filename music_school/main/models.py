from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class MyUser(AbstractUser):
  last_name = models.CharField("Фамилия", max_length = 50, blank=True, null=True)
  first_name = models.CharField("Имя", max_length = 50, blank=True, null=True)
  middle_name = models.CharField("Отчество", max_length = 50, blank=True, null=True)
  email = models.CharField("Эл. почта", max_length = 254, blank=True, null=True)
  phone = models.CharField('Номер телефона', max_length = 15, blank=True, null=True)
  birth_date = models.DateField("Дата рождения", blank=True, null=True)
  is_teacher = models.BooleanField("Учитель", default=False, null=True)

  def __str__(self):
    return f"{self.username}"