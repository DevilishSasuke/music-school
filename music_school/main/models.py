from django.db import models

# Create your models here.
class Person(models.Model):
  patient_id = models.AutoField(primary_key=True)
  last_name = models.CharField('Фамилия', max_length = 50)
  first_name = models.CharField('Имя', max_length = 50)
  middle_name = models.CharField('Отчество', max_length = 50)
  email = models.CharField("Эл. почта", max_length = 254)
  phone = models.CharField('Номер телефона', max_length = 15)
  birth_date = models.DateField('Дата рождения')

  def __str__(self):
    return f'{self.last_name} {self.first_name} {self.middle_name}'
  

class Pupil(Person):
  class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

class Teacher(Person):
  class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учители'