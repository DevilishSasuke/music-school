from django.urls import path
from . import views


urlpatterns = [
  path('', views.login, name='home'),
  path('/login', views.login, name='profile'),
  path('/register', views.register, name='calendar'),
]