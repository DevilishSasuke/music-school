from django.db import models
from yookassa import Payment as YooPayment

import uuid

class Payment(models.Model):
  user = models.CharField(max_length=150,)
  lesson = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

  def is_paid(username, lesson_id):
    payments = Payment.objects.filter(user=username, lesson=lesson_id)
    for payment in payments:
      yoo_id = str(payment.payment_id)
      yoopayment = YooPayment.find_one(yoo_id)
      
      if (yoopayment.status == "succeeded"):
        return True

    return False

  def __str__(self):
    return f'{self.payment_id}'