from django.urls import path
from . import views


urlpatterns = [
  path('', views.own_profile, name='own-profile'),
  path('<str:username>', views.profile, name='profile'),
  path('<str:username>/rate', views.rate, name='rate'),
]