from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        # Check for uniqueness on update
        instance = self.instance
        if instance and Employee.objects.exclude(pk=instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        elif not instance and Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        
        return value.lower()
    
    def validate(self, data):
        # Additional cross-field validation if needed
        return data