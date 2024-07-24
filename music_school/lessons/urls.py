from django.urls import path
from . import views


urlpatterns = [
  path('', views.lessons, name='lessons'),
  path('<int:number>', views.lesson, name='lesson'),
  path('calendar/', views.calendar, name='calendar'),
  path('add/', views.add_lesson, name='add-lesson')
]