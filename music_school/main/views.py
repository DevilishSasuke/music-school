from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BugForm

from .models import MyUser

from django.core.mail import send_mail
from django.contrib import messages

from dotenv import load_dotenv
from os import getenv

load_dotenv()

def home(request): 
  if request.user.is_authenticated:
    username = request.user.username
  else:
    username = ''

  data = {
    "title": "Главная страница",
    "username": username,
  }

  return render(request, 'home.html', data)

@login_required
def calendar(request):
  
  data = {
    "title": "Календарь заданий",
  }

  pass

@login_required
def chat(request):

  data = {
    "title": "Мои чаты",
  }

  pass

@login_required
def lessons(request):

  data = {
    "title": "Мои уроки",
  }
  
  pass

@login_required
def rating(request):
  users = MyUser.objects.all()
  users = sorted(users, key=lambda user: user.rating, reverse=True)

  data = {
    "title": "Рейтинг пользователей",
    "users": users,
  }

  return render(request, "rating.html", data)



@login_required
def pay(request):

  data = {
    "title": "Оплата",
  }

  pass

def bug(request):
  if  request.method == 'POST':
    form = BugForm(request.POST)
    if form.is_valid():
      user_email = form.cleaned_data['user_email']
      user_msg = form.cleaned_data['text']
      send_bug_report(user_email, user_msg)

  form = BugForm()

  data = {
    'title': 'Сообщение об ошибке',
    'form': form,
  }

  return render(request, 'bug.html', data)


def send_bug_report(email, text):
  subject = "Bug report"
  message = f'Bug report from {email}:\n\n {text}'
  sender = getenv("CORPORATE_EMAIL")
  recipient = [getenv("ADMIN_EMAIL")]

  send_mail(subject, message, sender, recipient)
  