from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Message
from main.models import MyUser


@login_required
def chats(request):
  user = request.user
  user.update_online()

  usernames = Message.get_chat_list_usernames(user.username)

  users = list()
  for username in usernames:
    users.append(MyUser.get_user_by_username(username))

  data = {
    "title": "Список чатов",
    "users": users,
  }

  return render(request, "chats.html", data)

@login_required
def chat(request, username):
  user = request.user
  user.update_online()
  
  if user.username == username:
    messages.error(request, f'You can\'t chat with yourself')
    return redirect("home")
  
  other_user = MyUser.get_user_by_username(username=username)

  if not other_user:
    messages.error(request, f"There is no such a user: {username}")
    return redirect("home")
  
  if request.method == "POST":
    message = request.POST['msg_text']

    new_msg = Message(sender=user.username, reciever=username, message=message)
    new_msg.save()
  
  msgs = Message.get_messages_for_chat(user.username, username)

  data = {
    "title": f"Чат с {username}" ,
    "user": user,
    "messages": msgs,
  }
  
  return render(request, "chat.html", data)