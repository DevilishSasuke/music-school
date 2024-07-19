from django.contrib import admin
from .models import MyUser, RatingLog

admin.site.register(MyUser)
admin.site.register(RatingLog)