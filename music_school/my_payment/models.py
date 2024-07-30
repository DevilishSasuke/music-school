from django.db import models

class Payment(models.Model):
  user = models.CharField(max_length=150,)
  lesson = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)

  def is_paid(username, lesson_id):
    return Payment.objects.filter(user=username, lesson=lesson_id).exists()

  def __str__(self):
    return f'{self.user} payed for lesson {self.lesson} at {self.timestamp}'