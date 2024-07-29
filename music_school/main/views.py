from django.core.mail import send_mail # mail sender for bugs
from django.contrib import messages # error messages on page

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#environment vars
from dotenv import load_dotenv
from os import getenv

from .forms import BugForm

from .models import MyUser


load_dotenv() # load all env vars

def home(request):
  username = request.user.username

  data = {
    "title": "Главная страница",
    "username": username,
  }

  return render(request, 'home.html', data)



@login_required
def chat(request):

  data = {
    "title": "Мои чаты",
  }

  pass



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
      messages.success(request, f'Thanks for your request, {user_email}')
      return redirect("home")
    else:
      for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{error}")


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
  