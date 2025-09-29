from django.urls import path
from .views import GoalListView, GoalDetailView

urlpatterns = [
    path('employees/<int:employee_id>/goals/', GoalListView.as_view(), name='employee_goals'),
    path('goals/<int:id>/', GoalDetailView.as_view(), name='goal_detail'),
]
