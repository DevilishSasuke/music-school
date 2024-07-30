from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from lessons.models import Lesson
from .models import Payment

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

  return render(request, "pay.html", data)

def payments(request):
  return redirect("bug")