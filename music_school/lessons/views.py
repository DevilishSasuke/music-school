from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import MyUser

@login_required
def lessons(request):
  user = MyUser.get_user_by_username(username=request.user.username)
  is_teacher = user.is_teacher

  data = {
    "title": "Мои уроки",
  }
  
  return render(request, "layout.html", data)

@login_required
def calendar(request):
  
  data = {
    "title": "Календарь заданий",
  }

  return render(request, "layout.html", data)



@login_required
def lesson(request, number):
  user = MyUser.get_user_by_username(username=request.user.username)
  is_teacher = user.is_teacher

  data = {
    "title": "Урок: " #{lesson.title}
  }

  return render(request, "layout.html", data)
