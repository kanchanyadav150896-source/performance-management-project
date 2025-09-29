from django.urls import path
from .views_outliers import PerformanceOutlierAPIView

urlpatterns = [
    path('performance/outliers/', PerformanceOutlierAPIView.as_view()),
]
