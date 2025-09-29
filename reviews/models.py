from django.db import models
from users.models import Employee

class ReviewCycle(models.Model):
    STATUS_CHOICES = [('active','Active'),('closed','Closed')]
    name = models.CharField(max_length=20)  # e.g., "2024 Q1"
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

class Review(models.Model):
    REVIEW_TYPE = [('self','Self'),('manager','Manager'),('peer','Peer')]
    STATUS = [('draft','Draft'),('submitted','Submitted')]

    employee = models.ForeignKey(Employee, related_name='reviews_received', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, related_name='reviews_given', on_delete=models.CASCADE)
    cycle = models.ForeignKey(ReviewCycle, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPE)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    submitted_date = models.DateTimeField(null=True, blank=True)

class Score(models.Model):
    CRITERIA_CHOICES = [('technical','Technical'),('communication','Communication'),
                        ('leadership','Leadership'),('goals','Goals')]
    review = models.ForeignKey(Review, related_name='scores', on_delete=models.CASCADE)
    criteria = models.CharField(max_length=20, choices=CRITERIA_CHOICES)
    score = models.IntegerField()
    comments = models.TextField(blank=True)
