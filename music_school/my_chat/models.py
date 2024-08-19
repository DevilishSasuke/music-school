from django.db import models

# Create your models here.
class Message(models.Model):
  sender = models.CharField(max_length=150,)
  reciever = models.CharField(max_length=150,)
  message = models.TextField()

  def __str__(self):
    return f'{self.sender} - {self.reciever} - {self.message[:10]}'