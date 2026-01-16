from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee

class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'department': 'Engineering',
            'role': 'Developer'
        }
        
        self.employee = Employee.objects.create(
            name='Jane Smith',
            email='jane.smith@example.com',
            department='HR',
            role='Manager'
        )
    
    def test_create_employee_success(self):
        response = self.client.post('/api/employees/', self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['email'], 'john.doe@example.com')
    
    def test_create_employee_duplicate_email(self):
        duplicate_data = self.employee_data.copy()
        duplicate_data['email'] = 'jane.smith@example.com'
        response = self.client.post('/api/employees/', duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_create_employee_empty_name(self):
        invalid_data = self.employee_data.copy()
        invalid_data['name'] = ''
        response = self.client.post('/api/employees/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_create_employee_invalid_email(self):
        invalid_data = self.employee_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post('/api/employees/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_list_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_retrieve_employee_success(self):
        response = self.client.get(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'jane.smith@example.com')
    
    def test_retrieve_employee_not_found(self):
        response = self.client.get('/api/employees/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_employee_success(self):
        update_data = {
            'name': 'Jane Updated',
            'email': 'jane.updated@example.com',
            'department': 'Sales',
            'role': 'Manager'
        }
        response = self.client.put(f'/api/employees/{self.employee.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Jane Updated')
        self.assertEqual(response.data['department'], 'Sales')
    
    def test_update_employee_not_found(self):
        response = self.client.put('/api/employees/99999/', self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_employee_success(self):
        response = self.client.delete(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
    
    def test_delete_employee_not_found(self):
        response = self.client.delete('/api/employees/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filter_by_department(self):
        response = self.client.get('/api/employees/?department=HR')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for employee in response.data['results']:
            self.assertEqual(employee['department'], 'HR')
    
    def test_filter_by_role(self):
        response = self.client.get('/api/employees/?role=Manager')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for employee in response.data['results']:
            self.assertEqual(employee['role'], 'Manager')
    
    def test_pagination(self):
        # Create more employees for pagination test
        for i in range(15):
            Employee.objects.create(
                name=f'Employee {i}',
                email=f'employee{i}@example.com',
                department='Engineering',
                role='Developer'
            )
        
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        
        response_page2 = self.client.get('/api/employees/?page=2')
        self.assertEqual(response_page2.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response_page2.data['results']), 0)
    
    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)