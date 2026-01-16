from django.db import models
from django.core.validators import EmailValidator

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('Engineering', 'Engineering'),
        ('Sales', 'Sales'),
        ('Marketing', 'Marketing'),
        ('Finance', 'Finance'),
    ]
    
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Analyst', 'Analyst'),
        ('Designer', 'Designer'),
        ('Consultant', 'Consultant'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )
    date_joined = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['department']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.email}"