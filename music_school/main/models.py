from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class MyUser(AbstractUser):
  last_name = models.CharField("Фамилия", max_length = 50, blank=True, null=True)
  first_name = models.CharField("Имя", max_length = 50, blank=True, null=True)
  middle_name = models.CharField("Отчество", max_length = 50, blank=True, null=True)
  email = models.CharField("Эл. почта", max_length = 254, blank=True, null=True)
  phone = models.CharField('Номер телефона', max_length = 15, blank=True, null=True)
  birth_date = models.DateField("Дата рождения", blank=True, null=True)
  is_teacher = models.BooleanField("Учитель", default=False, null=True)
  total_rating = models.IntegerField("Общий счёт рейтинга", default=0, blank=True)
  rating_count = models.IntegerField("Количество оценивших", default=0, blank=True)
  last_online = models.DateTimeField("Последний онлайн", blank=True, null=True)

  @property
  def rating(self):
    if self.rating_count == 0:
      return 0.0
    return round(self.total_rating / self.rating_count, 2)
  
  @property
  def rating_percentage(self):
     return int(self.rating / 5 * 100)
  
  def get_user_by_username(username):
    try:
        user = MyUser.objects.get(username=username)
        return user
    except MyUser.DoesNotExist:
        return None
    
  def update_online(self):
     self.last_online = timezone.now()
     self.save()

  def __str__(self):
    return self.username


class RatingLog(models.Model):
   sender = models.CharField(max_length=150,)
   reciever = models.CharField(max_length=150)
   rating = models.IntegerField()
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return f'{self.sender} rated {self.reciever} - {self.rating}'
   
   def get_rate_log(sender_name, reciever_name):
      try:
         log = RatingLog.objects.get(sender=sender_name, reciever=reciever_name)
         return log
      except RatingLog.DoesNotExist:
         return None

