from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import MyUser, RatingLog

from .forms import UserInfoForm, RateForm

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