from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('reviews.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/', include('reviews.urls_outliers')),
]
