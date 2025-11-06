from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ip/', include('ip_tracking.urls')),  # All IP tracking URLs
]
