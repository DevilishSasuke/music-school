from django.urls import path
from . import views


urlpatterns = [
  path('', views.chats, name='chats'),
  path('<str:username>', views.chat, name='chat'),
]