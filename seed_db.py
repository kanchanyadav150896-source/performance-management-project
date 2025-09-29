import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techcorp_performance.settings')
django.setup()

from users.models import Employee, User
from reviews.models import ReviewCycle, Review, Score
from goals.models import Goal
from django.contrib.auth.hashers import make_password

# Create 20 employees
departments = ['Engineering', 'Marketing', 'HR', 'Sales']
roles = ['employee', 'manager', 'hr']

employees = []
for i in range(1, 21):
    emp = Employee.objects.create(
        name=f'Employee {i}',
        email=f'employee{i}@techcorp.com',
        department=random.choice(departments),
        hire_date=date(2020,1,1) + timedelta(days=i*30),
        role=random.choice(roles)
    )
    employees.append(emp)
    User.objects.create(
        employee=emp,
        username=f'user{i}',
        password_hash=make_password('password123'),
        role=random.choice(roles)
    )

# Create 2 review cycles
for q in ['2024 Q1','2024 Q2']:
    cycle = ReviewCycle.objects.create(
        name=q,
        start_date=date(2024,1,1),
        end_date=date(2024,3,31),
        status='closed'
    )
    for emp in employees:
        # Self review
        review = Review.objects.create(
            employee=emp,
            reviewer=emp,
            cycle=cycle,
            review_type='self',
            status='submitted'
        )
        for crit in ['technical','communication','leadership','goals']:
            Score.objects.create(
                review=review,
                criteria=crit,
                score=random.randint(6,10),
                comments='Sample comment'
            )
        # Manager review (random manager)
        manager = random.choice([e for e in employees if e.role=='manager'])
        review = Review.objects.create(
            employee=emp,
            reviewer=manager,
            cycle=cycle,
            review_type='manager',
            status='submitted'
        )
        for crit in ['technical','communication','leadership','goals']:
            Score.objects.create(
                review=review,
                criteria=crit,
                score=random.randint(6,10),
                comments='Sample comment'
            )
