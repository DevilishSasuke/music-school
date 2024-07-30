from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('profile/', include('my_profile.urls')),
    path('lessons/', include('lessons.urls')),
    path('pay/', include('my_payment.urls')),
    path('auth/', include('my_auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
