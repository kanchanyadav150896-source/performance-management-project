from django.db import models
from users.models import Employee
from reviews.models import ReviewCycle

class Goal(models.Model):
    STATUS_CHOICES = [('not_started','Not Started'),('in_progress','In Progress'),('completed','Completed')]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE)
    description = models.TextField()
    target_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    progress = models.IntegerField()  # 0-100
