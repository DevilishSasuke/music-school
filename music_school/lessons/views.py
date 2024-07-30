from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from main.models import MyUser
from my_payment.models import Payment
from .models import Lesson
from .forms import LessonForm

import calendar

LESSON_AMOUNT_ON_PAGE = 3 * 2

@login_required
def lessons(request):
  user = request.user
  user.update_online()

  if user.is_teacher:
    lessons = Lesson.get_lessons_by_teacher(user.username)
  else:
    lessons = Lesson.get_lessons_by_subscriptions(user.username)

  if lessons:
    lessons = lessons.order_by("date")[:6]
    empty_slots = [0] * (LESSON_AMOUNT_ON_PAGE - len(lessons))
  else:
    empty_slots = [0] * LESSON_AMOUNT_ON_PAGE

  data = {
    "title": "Мои уроки",
    "user": user,
    "lessons": lessons,
    "empty_slots": empty_slots,
  }
  
  return render(request, "lessons.html", data)

@login_required
def my_calendar(request):
  request.user.update_online()
  today = timezone.now().date()
  cal = calendar.monthcalendar(today.year, today.month)
  week_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
  
  lessons = Lesson.get_this_month_lessons(request.user.username)

  # dict of lessons corresponding to the days
  # if 2 or more in 1 day
  # the first lesson is shown
  lesson_days = {}
  for lesson in reversed(lessons):
    lesson_days[lesson.date.day] = lesson

  # list of days
  # for correct calendar display on html page
  # and for url binding
  days_with_ids = []
  for week in cal:
    for day in week:
      if day in lesson_days:
        days_with_ids.append(MyDay(day, lesson_days[day]))
      else:
        days_with_ids.append(MyDay(day))

  data = {
    "today": today,
    "week_days": week_days,
    "days": days_with_ids,
  }

  return render(request, "calendar.html", data)



@login_required
def lesson(request, number):
  user = request.user
  user.update_online()
  lesson = Lesson.get_lesson_by_id(number)
  is_lesson_owner = request.user.username == lesson.teacher
  is_paid = Payment.is_paid(user.username, number)

  if not lesson:
    messages.error(request, f"No such a lesson")
    return redirect("home")
  
  data = {
    "title": "Урок: " + lesson.title[0:20],
    "user": user,
    "lesson": lesson,
    "is_paid": is_paid, 
  } 

  if not user.is_teacher:
    return render(request, "lesson.html", data)

  if not is_lesson_owner:
    messages.error(request, "You have no right to check this page")
    return redirect("home")
  
  form = LessonForm(instance=lesson)
  if request.method == "POST":
    form = LessonForm(request.POST, request.FILES, instance=lesson)

    if form.is_valid():
      cur_form = form.save(commit=False)
      lesson.teacher = request.user.username
      lesson.date = cur_form.date
      lesson.title = cur_form.title
      lesson.description = cur_form.description
      lesson.price = cur_form.price
      if "file" in request.FILES:
        lesson.file = request.FILES["file"]

      lesson.save()
      return redirect("lesson", lesson.id)
    else:
      for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{error}")

  data["form"] = form

  return render(request, "add-lesson.html", data)

@login_required
def add_lesson(request):
  user = request.user
  user.update_online()

  if not user.is_teacher:
    return redirect("home")
  
  form = LessonForm()
  if request.method == "POST":
    form = LessonForm(request.POST, request.FILES)

    if form.is_valid():
      cur_form = form.save(commit=False)
      lesson = Lesson.objects.create(
        teacher=request.user.username,
        date=cur_form.date,
        title=cur_form.title,
        description=cur_form.description,
        price=cur_form.price,
      )

      if "file" in request.FILES:
        lesson.file = request.FILES["file"]
      lesson.save()

      return redirect("lessons")
    else:
      for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{error}")

  data = {
    "title": "Добавить урок",
    "user": user,
    "form": form,
  }

  return render(request, "add-lesson.html", data)


class MyDay:
  def __init__(self, number, lesson=None):
    self.number = number
    self.lesson = lesson