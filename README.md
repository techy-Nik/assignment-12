# FastAPI Calculator with User Authentication & BREAD Operations

A production-ready REST API calculator built with FastAPI, featuring user authentication, complete BREAD (Browse, Read, Edit, Add, Delete) operations, polymorphic SQLAlchemy models, and comprehensive test coverage.

## 🎯 Project Overview

This project demonstrates advanced Python web development concepts including:

- **User Authentication** - Registration and login with password hashing
- **BREAD Operations** - Complete REST API for calculation management
- **Polymorphic Inheritance** - SQLAlchemy single-table inheritance for calculation types
- **Data Validation** - Pydantic schemas with custom validators
- **Test-Driven Development** - Comprehensive integration and unit tests
- **Docker Support** - Containerized application with Docker Compose
- **OpenAPI Documentation** - Interactive API documentation with Swagger UI

## ✨ Features

### User Management
✅ User registration with secure password hashing  
✅ User login with password verification  
✅ Session/token tracking (optional authentication)

### Calculation Operations (BREAD)
✅ **Browse** - List all calculations (`GET /calculations`)  
✅ **Read** - Get specific calculation (`GET /calculations/{id}`)  
✅ **Edit** - Update calculation (`PUT/PATCH /calculations/{id}`)  
✅ **Add** - Create new calculation (`POST /calculations`)  
✅ **Delete** - Remove calculation (`DELETE /calculations/{id}`)

### Calculation Types
✅ Addition, Subtraction, Multiplication, Division  
✅ Division by zero protection  
✅ User association with calculations  
✅ Polymorphic model structure

### Technical Features
✅ PostgreSQL database integration  
✅ Docker containerization  
✅ FastAPI with automatic OpenAPI documentation  
✅ Comprehensive error handling

## 🏗️ Architecture

### API Endpoints

#### User Endpoints
- `POST /users/register` - Register new user
- `POST /users/login` - User login

#### Calculation Endpoints (BREAD)
- `GET /calculations` - Browse all calculations
- `GET /calculations/{id}` - Read specific calculation
- `POST /calculations` - Add new calculation
- `PUT /calculations/{id}` - Edit calculation (full update)
- `PATCH /calculations/{id}` - Edit calculation (partial update)
- `DELETE /calculations/{id}` - Delete calculation

### Project Structure

```
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── redis.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── database.py
│   ├── database_init.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── calculation.py
│   │   └── user.py
│   ├── operations
│   │   └── __init__.py
│   └── schemas
│       ├── __init__.py
│       ├── base.py
│       ├── calculation.py
│       ├── token.py
│       └── user.py
├── docker-compose.yml
├── init-db.sh
├── pytest.ini
├── requirements.txt
├── templates
│   └── index.html
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── e2e
    │   ├── __init__.py
    │   ├── test_e2e.bk
    │   └── test_fastapi_calculator.py
    ├── integration
    │   ├── __init__.py
    │   ├── test_calculation.py
    │   ├── test_calculation_schema.py
    │   ├── test_database.py
    │   ├── test_dependencies.py
    │   ├── test_jwt.py
    │   ├── test_redis.py
    │   ├── test_schema_base.py
    │   ├── test_user.py
    │   └── test_user_auth.py
    └── unit
        ├── __init__.py
        └── test_calculator.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Docker Desktop
- Git

### Installation

#### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/techy-Nik/assignment-12.git
   cd assignment-12
   ```

2. **Start the application with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - API Base URL: http://localhost:8000

#### Option 2: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/techy-Nik/assignment-12.git
   cd assignment-12
   ```

2. **Create and activate virtual environment**
   ```bash
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 🧪 Running Tests

### Run All Tests Locally

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/integration/test_calculations_api.py -v
pytest tests/integration/test_users_api.py -v
```

### Integration Tests Coverage

The integration tests cover:

- ✅ User registration with validation
- ✅ User login with password verification
- ✅ Creating calculations (POST)
- ✅ Browsing calculations (GET all)
- ✅ Reading single calculation (GET by ID)
- ✅ Updating calculations (PUT/PATCH)
- ✅ Deleting calculations (DELETE)
- ✅ Division by zero validation
- ✅ Invalid input handling
- ✅ User-calculation associations

### View Coverage Report

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

## 🔍 Manual Testing with OpenAPI

### Accessing Interactive Documentation

1. **Start the application**
   ```bash
   docker-compose up
   # or
   uvicorn main:app --reload
   ```

2. **Open Swagger UI**
   - Navigate to: http://localhost:8000/docs
   - You'll see all available endpoints with "Try it out" buttons

3. **Alternative: ReDoc Interface**
   - Navigate to: http://localhost:8000/redoc
   - Clean, three-panel documentation interface

### Step-by-Step Manual Testing

#### 1. Register a New User

1. In Swagger UI, expand `POST /users/register`
2. Click "Try it out"
3. Enter request body:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "securepass123"
   }
   ```
4. Click "Execute"
5. Verify 201 response with user details

#### 2. Login

1. Expand `POST /users/login`
2. Click "Try it out"
3. Enter credentials:
   ```json
   {
     "username": "testuser",
     "password": "securepass123"
   }
   ```
4. Click "Execute"
5. Note the user_id for subsequent requests

#### 3. Create a Calculation (Add)

1. Expand `POST /calculations`
2. Click "Try it out"
3. Enter calculation data:
   ```json
   {
     "type": "addition",
     "user_id": 1,
     "inputs": [10, 20, 30]
   }
   ```
4. Click "Execute"
5. Verify 201 response with result: 60

#### 4. Browse All Calculations

1. Expand `GET /calculations`
2. Click "Try it out"
3. Click "Execute"
4. Verify list of calculations returned

#### 5. Read Specific Calculation

1. Expand `GET /calculations/{id}`
2. Click "Try it out"
3. Enter calculation ID (e.g., 1)
4. Click "Execute"
5. Verify calculation details returned

#### 6. Edit a Calculation

1. Expand `PUT /calculations/{id}` or `PATCH /calculations/{id}`
2. Click "Try it out"
3. Enter ID and updated data:
   ```json
   {
     "type": "multiplication",
     "inputs": [5, 10, 2]
   }
   ```
4. Click "Execute"
5. Verify updated calculation with result: 100

#### 7. Delete a Calculation

1. Expand `DELETE /calculations/{id}`
2. Click "Try it out"
3. Enter calculation ID
4. Click "Execute"
5. Verify 204 No Content response

#### 8. Test Validation (Division by Zero)

1. Expand `POST /calculations`
2. Try creating invalid calculation:
   ```json
   {
     "type": "division",
     "user_id": 1,
     "inputs": [10, 0]
   }
   ```
3. Click "Execute"
4. Verify 422 validation error: "Cannot divide by zero"

## 🐳 Docker Hub Repository

**Docker Image**: [techynik/module-12](https://hub.docker.com/repository/docker/techynik/module-12/general)

### Pull and Run from Docker Hub

```bash
# Pull the image
docker pull techynik/module-12:latest

# Run the container
docker run -p 8000:8000 techynik/module-12:latest
```

### Build and Push (For Maintainers)

```bash
# Build the image
docker build -t techynik/module-12:latest .

# Push to Docker Hub
docker push techynik/module-12:latest
```

## 💡 Usage Examples

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register user
response = requests.post(
    f"{BASE_URL}/users/register",
    json={
        "username": "john_doe",
        "email": "john@example.com",
        "password": "mypassword123"
    }
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/users/login",
    json={
        "username": "john_doe",
        "password": "mypassword123"
    }
)
user_data = response.json()
user_id = user_data["id"]

# Create calculation
response = requests.post(
    f"{BASE_URL}/calculations",
    json={
        "type": "multiplication",
        "user_id": user_id,
        "inputs": [5, 10, 2]
    }
)
calc = response.json()
print(f"Result: {calc['result']}")  # Result: 100

# Get all calculations
response = requests.get(f"{BASE_URL}/calculations")
calculations = response.json()

# Update calculation
response = requests.put(
    f"{BASE_URL}/calculations/{calc['id']}",
    json={
        "type": "addition",
        "inputs": [100, 200]
    }
)

# Delete calculation
response = requests.delete(f"{BASE_URL}/calculations/{calc['id']}")
```

### Using cURL

```bash
# Register user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}'

# Create calculation
curl -X POST "http://localhost:8000/calculations" \
  -H "Content-Type: application/json" \
  -d '{"type":"addition","user_id":1,"inputs":[10,20,30]}'

# Get all calculations
curl -X GET "http://localhost:8000/calculations"

# Get specific calculation
curl -X GET "http://localhost:8000/calculations/1"

# Update calculation
curl -X PUT "http://localhost:8000/calculations/1" \
  -H "Content-Type: application/json" \
  -d '{"type":"multiplication","inputs":[5,10]}'

# Delete calculation
curl -X DELETE "http://localhost:8000/calculations/1"
```

## 📦 Dependencies

Core dependencies:

- **FastAPI** - Modern web framework for APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using type hints
- **psycopg2-binary** - PostgreSQL adapter
- **passlib** - Password hashing utilities
- **pytest** - Testing framework
- **httpx** - HTTP client for testing

See `requirements.txt` for complete list.


### Docker Compose Configuration

The `docker-compose.yml` includes:
- FastAPI application container
- PostgreSQL database container
- Volume persistence for database
- Network configuration
- Environment variables

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Port Already in Use

```bash
# Find process using port 8000
# Mac/Linux
lsof -i :8000

# Windows
netstat -ano | findstr :8000

# Change port in docker-compose.yml if needed
```

### Tests Failing

```bash
# Ensure test database is clean
docker-compose down -v
docker-compose up -d

# Run tests with verbose output
pytest -vv
```

## 📚 API Schema Examples

### UserCreate Schema
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

### CalculationCreate Schema
```json
{
  "type": "addition|subtraction|multiplication|division",
  "user_id": 1,
  "inputs": [1, 2, 3]
}
```

### CalculationRead Schema
```json
{
  "id": 1,
  "type": "addition",
  "user_id": 1,
  "inputs": [1, 2, 3],
  "result": 6.0,
  "created_at": "2025-11-24T10:30:00"
}
```

## 🎓 Learning Objectives

This project demonstrates:

1. **RESTful API Design** - Implementing BREAD operations
2. **User Authentication** - Registration and login flows
3. **Password Security** - Hashing and verification
4. **Data Validation** - Pydantic schemas with custom validators
5. **Database Integration** - SQLAlchemy ORM with relationships
6. **Testing** - Integration and unit tests
7. **Documentation** - OpenAPI/Swagger automatic docs
8. **Containerization** - Docker and Docker Compose
9. **Design Patterns** - Factory, polymorphism, DTOs

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Nikunj** - [techy-Nik](https://github.com/techy-Nik)

- GitHub: [@techy-Nik](https://github.com/techy-Nik)
- Project Repository: [assignment-12](https://github.com/techy-Nik/assignment-12)
- Docker Hub: [techynik/module-12](https://hub.docker.com/repository/docker/techynik/module-12)



