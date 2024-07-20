from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserInfoForm, BugForm, RateForm

from .models import MyUser, RatingLog

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
def own_profile(request):
  username = request.user.username
  link = "/profile/" + username

  return redirect(link)

@login_required
def profile(request, username):
  profile_name = request.user.username
  is_owner = username == profile_name
  user = MyUser.get_user_by_username(username=username)

  form = None

  if is_owner:
    if request.method == "POST":
      form = UserInfoForm(request.POST, instance=request.user)

      if form.is_valid():
        form.save()
        return redirect("own-profile")
    else:
      form = UserInfoForm(instance=request.user)

  data = {
    "title": "Мой профиль",
    "user": user,
    "form": form,
    "is_owner": is_owner,
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
  users = MyUser.objects.all()
  users = sorted(users, key=lambda user: user.rating, reverse=True)

  data = {
    "title": "Рейтинг учителей",
    "users": users,
  }

  return render(request, "rating.html", data)

@login_required
def rate(request, username):
  # cannot rate urself
  if username == request.user.username:
    return redirect("home")
  
  user = MyUser.get_user_by_username(username=username)

  form = RateForm()
  if user:
    if request.method == "POST":
      log = RatingLog.get_rate_log(sender_name=request.user.username, reciever_name=username)
      form = RateForm(request.POST)
      # cannot be more than 1 user rate
      if log:
        messages.error(request, f'User {log.sender} already rated user {log.reciever}: {log.rating}')
        return redirect("rate", username=username)
      if form.is_valid():
        rating = int(form.cleaned_data["rating"])
        user.total_rating += rating
        user.rating_count += 1
        user.save()
        RatingLog.objects.create(sender=request.user.username, reciever=username, rating=rating)
        return redirect("home")
      
  data = {
    "title": "Оценить " + username,
    "user": user,
    "form": form,
  }

  return render(request, 'rate.html', data)

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
  