from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('profile/', views.own_profile, name='own-profile'),
  path('profile/<str:username>', views.profile, name='profile'),
  path('calendar/', views.calendar, name='calendar'),
  path('chat/', views.chat, name='chat'),
  path('lessons/', views.lessons, name='lessons'),
  path('rating/', views.rating, name='rating'),
  path('rate/<str:username>', views.rate, name='rate'),
  path('pay/', views.pay, name='pay'),
  path('bug/', views.bug, name='bug'),
]