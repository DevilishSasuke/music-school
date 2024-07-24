from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import MyUser
from .models import Lesson
from .forms import LessonForm

LESSON_AMOUNT_ON_PAGE = 3 * 2

@login_required
def lessons(request):
  user = MyUser.get_user_by_username(username=request.user.username)
  lessons = Lesson.objects.order_by('date')[:6]
  empty_slots = [0] * (LESSON_AMOUNT_ON_PAGE - len(lessons))

  data = {
    "title": "Мои уроки",
    "user": user,
    "lessons": lessons,
    "empty_slots": empty_slots,
  }
  
  return render(request, "lessons.html", data)

@login_required
def calendar(request):
  
  data = {
    "title": "Календарь заданий",
  }

  return render(request, "layout.html", data)



@login_required
def lesson(request, number):
  user = MyUser.get_user_by_username(username=request.user.username)
  lesson = Lesson.get_lesson_by_id(number)

  if not lesson:
    return redirect("home") 

  data = {
    "title": "Урок: ", #{lesson.title}
    "user": user,
  } 

  return render(request, "layout.html", data)

@login_required
def add_lesson(request):
  user = MyUser.get_user_by_username(username=request.user.username)

  if not user.is_teacher:
    return redirect("home")
  
  form = LessonForm()
  if request.method == "POST":
    form = LessonForm(request.POST)

    if form.is_valid():
      lesson = form.save(commit=False)
      lesson.teacher = request.user.username
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