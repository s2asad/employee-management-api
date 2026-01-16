from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'department', 'role', 'date_joined']
    list_filter = ['department', 'role', 'date_joined']
    search_fields = ['name', 'email']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email')
        }),
        ('Work Information', {
            'fields': ('department', 'role')
        }),
        ('System Information', {
            'fields': ('date_joined',)
        }),
    )