from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BugForm

from .models import MyUser

from django.core.mail import send_mail

from dotenv import load_dotenv
from os import getenv

load_dotenv()

def home(request): 

  data = {
    "title": "Главная страница",
  }

  return render(request, 'home.html', data)

@login_required
def profile(request):
  username = request.user.username
  user = MyUser.get_user_by_username(username=username)

  data = {
    "title": "Мой профиль",
    "user": user,
  }

  return render(request, 'profile.html', data)

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

  data = {
    "title": "Рейтинг учителей",
  }

  pass

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
  