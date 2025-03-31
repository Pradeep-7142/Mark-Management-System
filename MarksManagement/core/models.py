from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend User model to include roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Subject(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class Marks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.marks_obtained}/{self.total_marks})"
