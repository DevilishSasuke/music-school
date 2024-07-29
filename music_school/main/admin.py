from django.contrib import admin
from .models import MyUser, RatingLog, Subscription

admin.site.register(MyUser)
admin.site.register(RatingLog)
admin.site.register(Subscription)