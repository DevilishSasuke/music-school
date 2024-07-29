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

  if not user:
    messages.error(request, f"There is no such a user: {username}")
    return redirect("home")

  # show owner form with completed info
  if is_owner:
    if request.method == "POST":
      form = UserInfoForm(request.POST, instance=request.user)

      if form.is_valid():
        form.save()
        return redirect("own-profile")
      else:
        for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, f"{error}")
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
  # can't rate urself
  if username == request.user.username:
    messages.error(request, f'You can\'t rate yourself')
    return redirect("home")
  
  user = MyUser.get_user_by_username(username=username)

  form = RateForm()
  if user:
    if request.method == "POST":
      log = RatingLog.get_rate_log(sender_name=request.user.username, reciever_name=username)
      form = RateForm(request.POST)

      # can't rate the same user twice or more times
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
      else:
        for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, f"{error}")
      
  data = {
    "title": "Оценить " + username,
    "user": user,
    "form": form,
  }

  return render(request, 'rate.html', data)