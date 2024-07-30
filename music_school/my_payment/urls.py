from django.urls import path
from . import views


urlpatterns = [
  path('', views.payments, name='payments'),
  path('<int:lesson_id>', views.pay, name='pay'),
]