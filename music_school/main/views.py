from django.shortcuts import render
from .forms import BugForm

from django.core.mail import send_mail

from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Create your views here.
def home(request): 

  data = {
    "title": "Главная страница",
  }

  return render(request, 'home.html', data)

def profile(request):

  data = {
    "title": "Мой профиль",
  }

  return render(request, 'layout.html', data)

def calendar(request):
  
  data = {
    "title": "Календарь заданий",
  }

  pass

def chat(request):

  data = {
    "title": "Мои чаты",
  }

  pass

def lessons(request):

  data = {
    "title": "Мои уроки",
  }
  
  pass

def rating(request):

  data = {
    "title": "Рейтинг учителей",
  }

  pass

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
  