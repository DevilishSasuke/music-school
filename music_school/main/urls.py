from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('rating/', views.rating, name='rating'),
  path('bug/', views.bug, name='bug'),
]