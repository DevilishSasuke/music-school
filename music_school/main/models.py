from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
  last_name = models.CharField("Фамилия", max_length = 50, blank=True, null=True)
  first_name = models.CharField("Имя", max_length = 50, blank=True, null=True)
  middle_name = models.CharField("Отчество", max_length = 50, blank=True, null=True)
  email = models.CharField("Эл. почта", max_length = 254, blank=True, null=True)
  phone = models.CharField('Номер телефона', max_length = 15, blank=True, null=True)
  birth_date = models.DateField("Дата рождения", blank=True, null=True)
  is_teacher = models.BooleanField("Учитель", default=False, null=True)
  total_rating = models.IntegerField(default=0, blank=True)
  rating_count = models.IntegerField(default=0, blank=True)
  last_online = models.DateTimeField("Последний онлайн", blank=True, null=True)

  @property
  def rating(self):
    if self.rating_count == 0:
      return 0
    return self.total_rating / self.rating_count
  
  def get_user_by_username(username):
    try:
        user = MyUser.objects.get(username=username)
        return user
    except MyUser.DoesNotExist:
        return None

  def __str__(self):
    return self.username
  

'''
class Pupil(MyUser):
  class Meta:
    verbose_name = 'Ученик'
    verbose_name_plural = 'Ученики'

class Teacher(MyUser):
  class Meta:
    verbose_name = 'Учитель'
    verbose_name_plural = 'Учители'
'''