from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('chat/', views.chat, name='chat'),
  path('rating/', views.rating, name='rating'),
  path('bug/', views.bug, name='bug'),
]