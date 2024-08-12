from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from yookassa import Configuration
from yookassa import Payment as YooPayment
from uuid import uuid4
from decimal import Decimal

from lessons.models import Lesson
from .models import Payment


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
commission = settings.YOOKASSA_COMMISSION
LESSON_AMOUNT_ON_PAGE = 3 * 2

@login_required
def pay(request, lesson_id):
  user = request.user
  user.update_online()

  if user.is_teacher:
    messages.error(request, f"Only pupils can pay for lessons")
    return redirect("home")
  
  lesson = Lesson.get_lesson_by_id(lesson_id)
  if not Lesson:
    messages.error("No such a lesson")
    return redirect("home")
  
  is_paid = Payment.is_paid(user.username, lesson_id)
  if is_paid:
    messages.success(request, f"You have already paid for this lesson")
    return redirect("lesson", number=lesson_id)

  data = {
    "title": "Оплата урока",
    "user": user,
    "lesson": lesson,
  }

  if request.method == "POST":
    payment_type = request.POST.get("payment-type")

    if payment_type == "yookassa-payment":
      idempotence_key = uuid4()
      currency = "RUB"
      description = "Оплата урока" + str(lesson_id)
      lesson_price = price_with_commission(lesson.price, commission)
      return_url = request.build_absolute_uri(reverse('lesson', args=[lesson_id]))
      payment = YooPayment.create({
        "amount": {
          "value": str(lesson_price),
          "currency": currency,
        },
        "confirmation": {
          "type":"redirect",
          "return_url": return_url,
        },
        "capture": True,
        "test": True,
        "description": description
        }, idempotence_key)
      
      confirmation_url = payment.confirmation.confirmation_url

      my_payment = Payment.objects.create(
        user=user.username, 
        lesson=lesson_id, 
        price=lesson.price_with_commission, 
        payment_id=payment.id,
      )
      my_payment.save()

      return redirect(confirmation_url)

  return render(request, "pay.html", data)

@login_required
def payments(request):
  user = request.user
  user.update_online()

  if user.is_teacher:
    messages.error(request, f"You are teacher")
    return redirect("home")
  else:
    lessons = Lesson.get_lessons_by_subscriptions(user.username)

  lessons = lessons.order_by("date")
  unpaid_lessons = [lesson for lesson in lessons if not Payment.is_paid(user.username, lesson.id)]
  if unpaid_lessons:
    unpaid_lessons = unpaid_lessons[:6]
    empty_slots = [0] * (LESSON_AMOUNT_ON_PAGE - len(unpaid_lessons))
  else:
    empty_slots = [0] * LESSON_AMOUNT_ON_PAGE

  data = {
    "title": "Мои уроки",
    "user": user,
    "lessons": unpaid_lessons,
    "empty_slots": empty_slots,
  }
  
  return render(request, "payments.html", data)


def price_with_commission(price, commission):
  final_price = price * Decimal(1 + (commission / 100))
  return final_price.quantize(Decimal("1.00"))