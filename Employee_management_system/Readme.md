# Employee Management REST API

A Django REST Framework-based API for managing employee records with CRUD operations, authentication, filtering, and pagination.

## Features

-  Full CRUD operations for employees
-  JWT token-based authentication
-  Email validation and uniqueness enforcement
-  Filtering by department and role
-  Pagination (10 records per page)
-  Proper HTTP status codes
-  Comprehensive unit tests
-  RESTful design principles

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt

## Installation & Setup

### 1. Clone or Create Project Structure

```bash
# Create project directory
mkdir employee_management_api
cd employee_management_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Django Project

```bash
# Create Django project
django-admin startproject employee_management .

# Create employees app
python manage.py startapp employees
```

### 4. Apply Configurations

Copy the provided files to their respective locations:
- `settings.py` → `employee_management/settings.py`
- `urls.py` → `employee_management/urls.py`
- `models.py` → `employees/models.py`
- `serializers.py` → `employees/serializers.py`
- `views.py` → `employees/views.py`
- `tests.py` → `employees/tests.py`

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Authentication

### Obtain JWT Token

**Endpoint:** `POST /api/token/`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Token in Postman

1. Copy the `access` token from the response
2. In Postman, go to the **Authorization** tab
3. Select **Type: Bearer Token**
4. Paste the token in the **Token** field
5. All subsequent requests will include this token

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### 1. Create Employee

**Endpoint:** `POST /api/employees/`

**Headers:**
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2025-01-09"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["An employee with this email already exists."]
}
```

### 2. List All Employees

**Endpoint:** `GET /api/employees/`

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/employees/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "department": "Engineering",
      "role": "Developer",
      "date_joined": "2025-01-09"
    },
    // ... 9 more employees
  ]
}
```

### 3. Filter Employees

**By Department:**
```
GET /api/employees/?department=HR
```

**By Role:**
```
GET /api/employees/?role=Manager
```

**Combined Filters:**
```
GET /api/employees/?department=Engineering&role=Developer
```

### 4. Pagination

**Second Page:**
```
GET /api/employees/?page=2
```

### 5. Retrieve Single Employee

**Endpoint:** `GET /api/employees/{id}/`

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering",
  "role": "Developer",
  "date_joined": "2025-01-09"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Employee not found."
}
```

### 6. Update Employee

**Endpoint:** `PUT /api/employees/{id}/`

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "department": "Sales",
  "role": "Manager"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john.updated@example.com",
  "department": "Sales",
  "role": "Manager",
  "date_joined": "2025-01-09"
}
```

### 7. Delete Employee

**Endpoint:** `DELETE /api/employees/{id}/`

**Success Response:** `204 No Content` (empty body)

**Error Response (404 Not Found):**
```json
{
  "detail": "Employee not found."
}
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific test case
python manage.py test employees.tests.EmployeeAPITestCase.test_create_employee_success
```

## Validation Rules

1. **Name:** Required, cannot be empty or whitespace
2. **Email:** Required, must be valid email format, must be unique
3. **Department:** Optional, choices: HR, Engineering, Sales, Marketing, Finance
4. **Role:** Optional, choices: Manager, Developer, Analyst, Designer, Consultant
5. **Date Joined:** Auto-generated on creation, read-only

## HTTP Status Codes

- `200 OK` - Successful GET, PUT requests
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found

## Postman Collection Example

### Authentication Flow

1. **Get Token**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/token/`
   - Body: `{"username": "admin", "password": "admin123"}`
   - Save the access token

2. **Create Employee**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/employees/`
   - Auth: Bearer Token (paste access token)
   - Body: Employee JSON

3. **List Employees**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/`
   - Auth: Bearer Token

4. **Filter by Department**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/employees/?department=Engineering`
   - Auth: Bearer Token

5. **Update Employee**
   - Method: PUT
   - URL: `http://127.0.0.1:8000/api/employees/1/`
   - Auth: Bearer Token
   - Body: Updated employee JSON

6. **Delete Employee**
   - Method: DELETE
   - URL: `http://127.0.0.1:8000/api/employees/1/`
   - Auth: Bearer Token

## Project Structure

```
employee_management_api/
├── employee_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── employees/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify virtual environment is activated

**2. Authentication Error**
- Check token is included in Authorization header
- Verify token hasn't expired (default: 5 hours)
- Generate new token if needed

**3. Migration Errors**
- Delete db.sqlite3 and migrations folder (except __init__.py)
- Run `python manage.py makemigrations` and `python manage.py migrate`

**4. Port Already in Use**
- Change port: `python manage.py runserver 8080`

## Additional Notes

- Default pagination is 10 employees per page
- JWT access tokens expire after 5 hours
- All timestamps are in UTC
- Email addresses are case-insensitive (stored as lowercase)

## License

This project is created for HabotConnect hiring assessment.