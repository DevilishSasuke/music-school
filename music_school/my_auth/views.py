from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm 
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth


def register(request):
  if request.user.is_authenticated:
    return redirect("home")
  
  form = RegistrationForm()

  if (request.method == "POST"):
    form = RegistrationForm(request.POST)

    if form.is_valid():
      try:
        form.save()
        return redirect("/")
      except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    else:
      for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{error}")
  
  data = {
    "title": "Регистрация",
    "form": form,
  } 

  return render(request, "register.html", data)

def login(request):
  if request.user.is_authenticated:
    return redirect("home")

  form = LoginForm()

  if request.method == "POST":
    form = LoginForm(request, data = request.POST)

    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")

      user = authenticate(request, username=username, password=password)
      if user is not None:
        auth.login(request, user)
        return redirect("/")
      else:
        for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, f"{error}")
    else:
      for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, f"{error}")

  data = {
    "title": "Вход в систему",
    "form": form,
  }

  return render(request, "login.html", data)

def logout(request):
  auth.logout(request)
  return redirect("home")