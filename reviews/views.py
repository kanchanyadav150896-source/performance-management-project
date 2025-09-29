from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, Score, ReviewCycle
from .serializers import ReviewSerializer, ScoreSerializer, ReviewCycleSerializer
from users.models import Employee
from goals.models import Goal
from django.utils import timezone
from django.db.models import Avg
import numpy as np

# ----------------- BUSINESS LOGIC ------------------
def calculate_final_score(employee_id, cycle_id):
    reviews = Review.objects.filter(employee_id=employee_id, cycle_id=cycle_id, status='submitted')
    if not reviews.exists():
        return 0.0
    manager_score = reviews.filter(review_type='manager').aggregate(avg=Avg('scores__score'))['avg'] or 0
    self_score = reviews.filter(review_type='self').aggregate(avg=Avg('scores__score'))['avg'] or 0
    peer_scores = reviews.filter(review_type='peer').aggregate(avg=Avg('scores__score'))['avg'] or 0
    final_score = (manager_score*0.5) + (self_score*0.3) + (peer_scores*0.2)
    return round(final_score,2)

def calculate_goal_achievement(employee_id, cycle_id):
    goals = Goal.objects.filter(employee_id=employee_id, cycle_id=cycle_id)
    if not goals.exists():
        return 0.0
    total_progress = sum([g.progress for g in goals])
    avg_progress = total_progress/goals.count()
    return round(avg_progress,2)

def get_performance_trend(employee_id, num_cycles=3):
    cycles = ReviewCycle.objects.order_by('-start_date')[:num_cycles]
    trend = []
    for cycle in reversed(cycles):
        score = calculate_final_score(employee_id, cycle.id)
        trend.append({'cycle': cycle.name, 'score': score})
    return trend

def identify_outliers(department):
    employees = Employee.objects.filter(department=department)
    scores = []
    emp_scores = {}
    for emp in employees:
        score = calculate_final_score(emp.id, ReviewCycle.objects.latest('id').id)
        scores.append(score)
        emp_scores[emp.id] = score
    if not scores:
        return []
    mean = np.mean(scores)
    std = np.std(scores)
    threshold = 1.5*std
    results = [{'employee_id': emp_id, 'score': score} for emp_id, score in emp_scores.items() if abs(score-mean)>threshold]
    return results

# ----------------- API VIEWS ------------------
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewSubmitView(APIView):
    def put(self, request, id):
        try:
            review = Review.objects.get(id=id)
            review.status = 'submitted'
            review.submitted_date = timezone.now()
            review.save()
            return Response({'message':'Review submitted'}, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({'error':'Review not found'}, status=status.HTTP_404_NOT_FOUND)

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

class EmployeeReviewHistoryView(APIView):
    def get(self, request, id):
        reviews = Review.objects.filter(employee_id=id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class BulkImportView(APIView):
    def post(self, request):
        reviews = request.data.get('reviews', [])
        created = []
        for rev in reviews:
            serializer = ReviewSerializer(data=rev)
            if serializer.is_valid():
                serializer.save()
                created.append(serializer.data)
        return Response({'created': created}, status=status.HTTP_201_CREATED)


from django.core.cache import cache

def get_department_summary(dept):
    cache_key = f"dept_summary_{dept}"
    summary = cache.get(cache_key)
    if summary is None:
        # Expensive DB query
        employees = Employee.objects.filter(department=dept)
        summary = []
        for emp in employees:
            score = calculate_final_score(emp.id, ReviewCycle.objects.latest('id').id)
            summary.append({'employee_id': emp.id, 'score': score})
        cache.set(cache_key, summary, 60*5)  # Cache for 5 minutes
    return summary
