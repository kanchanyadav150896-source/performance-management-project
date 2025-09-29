from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    hire_date = models.DateField()
    role = models.CharField(max_length=20)  # employee, manager, hr

    def __str__(self):
        return self.name

class User(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20)  # employee, manager, hr

    def __str__(self):
        return self.username
