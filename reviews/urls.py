from django.urls import path
from .views import ReviewCreateView, ReviewSubmitView, ReviewDetailView, EmployeeReviewHistoryView, BulkImportView

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view()),
    path('reviews/<int:id>/submit/', ReviewSubmitView.as_view()),
    path('reviews/<int:id>/', ReviewDetailView.as_view()),
    path('employees/<int:id>/reviews/', EmployeeReviewHistoryView.as_view()),
    path('reviews/bulk-import/', BulkImportView.as_view()),
]
