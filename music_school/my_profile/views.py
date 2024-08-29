from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from main.models import MyUser, RatingLog, Subscription

from .forms import UserInfoForm, RateForm

@login_required
def own_profile(request):
  request.user.update_online()

  username = request.user.username

  return redirect("profile", username=username)

@login_required
def profile(request, username):
  request.user.update_online()

  profile_name = request.user.username
  is_owner = username == profile_name
  sub = Subscription.get_sub(request.user.username, username)
  form = None

  if is_owner:
    user = request.user
  else:
    user = MyUser.get_user_by_username(username=username)

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
    "sub": sub,
    "is_owner": is_owner,
  }

  return render(request, 'profile.html', data)

@login_required
def rate(request, username):
  request.user.update_online()

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

@login_required
def sub(request, teacher_usrnm):
  request.user.update_online()

  pupil = request.user
  teacher = MyUser.get_user_by_username(teacher_usrnm)
  sub = Subscription.get_sub(pupil.username, teacher_usrnm)

  if pupil.is_teacher or not teacher.is_teacher:
    messages.error(request, f'Only pupil can subscribe on teacher')
    return redirect("profile",  username=teacher_usrnm)

  if sub:
    messages.error(request, f'You already subscribed on {teacher_usrnm}')
    return redirect("profile",  username=teacher_usrnm)

  Subscription.objects.create(pupil=pupil.username, teacher=teacher_usrnm)
  messages.success(request, f'You successfully subscribed on {teacher_usrnm}')
  
  return redirect("profile",  username=teacher_usrnm)

@login_required
def unsub(request, teacher_usrnm):
  request.user.update_online()

  pupil = request.user
  sub = Subscription.get_sub(pupil.username, teacher_usrnm)

  if sub:
    sub.delete()
    messages.success(request, f'You successfully unsubscribed on {teacher_usrnm}')
  else:
    messages.error(request, f'You have no subscription on {teacher_usrnm}')

  return redirect("profile",  username=teacher_usrnm)
