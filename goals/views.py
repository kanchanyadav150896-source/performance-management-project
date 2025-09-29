from rest_framework import generics
from .models import Goal
from .serializers import GoalSerializer

class GoalListView(generics.ListAPIView):
    serializer_class = GoalSerializer
    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return Goal.objects.filter(employee_id=employee_id)

class GoalDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    lookup_field = 'id'
