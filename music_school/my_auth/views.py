from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm 

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth


def register(request):
  form = RegistrationForm()

  if (request.method == "POST"):
    form = RegistrationForm(request.POST)

    if form.is_valid():
      try:
        form.save()

        return redirect("/")
      except Exception as e:
        pass
  
  data = {
    "title": "Регистрация",
    "form": form,
  } 

  return render(request, "register.html", data)

def login(request):
  form = LoginForm()

  if request.method == "POST":
    form = LoginForm(request, data = request.POST)

    if form.is_valid():
      user_email = request.POST.get("user_email")
      password = request.POST.get("password")

      user = authenticate(request, user_email=user_email, password=password)
      if user is not None:
        auth.login(request, user)
        return redirect("/")

  data = {
    "title": "Вход в систему",
    "form": form,
  }

  return render(request, "login.html", data)

def logout(request):
  auth.logout(request)
  return redirect("/")