Module 10: Secure User Authentication with SQLAlchemy
Show Image
📋 Project Overview
This project implements a secure user authentication system using FastAPI, SQLAlchemy, and bcrypt password hashing. It demonstrates fundamental web security practices including password hashing, database modeling with ORM, and input validation with Pydantic schemas.
🚀 Features

User Model: SQLAlchemy model with username, email, password_hash, and created_at fields
Password Security: Bcrypt hashing with unique salts for each password
Input Validation: Pydantic schemas with email format and password strength validation
Database: PostgreSQL with unique constraints on username and email
Comprehensive Testing: 43 tests covering unit, integration, and E2E scenarios
CI/CD Pipeline: Automated testing, security scanning, and Docker deployment

🏗️ Project Structure
assignment10/
├── app/
│   ├── models/
│   │   └── user.py              # SQLAlchemy User model
│   ├── schemas/
│   │   ├── base.py              # Pydantic base schemas with validation
│   │   └── user.py              # User schemas (UserCreate, UserRead)
│   ├── utils/
│   │   └── security.py          # Password hashing functions
│   ├── config.py                # Configuration settings
│   └── database.py              # Database connection setup
├── tests/
│   ├── unit/                    # Unit tests (30 tests)
│   ├── integration/             # Integration tests (10 tests)
│   └── e2e/                     # End-to-end tests (3 tests)
├── docker-compose.yml           # Local development setup
├── Dockerfile                   # Production container
└── requirements.txt             # Python dependencies
🔧 Local Setup
Prerequisites

Python 3.10+
Docker and Docker Compose
Git

Installation Steps

Clone the repository

bashgit clone https://github.com/Pruthul15/assignment10.git
cd assignment10

Create virtual environment

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

bashpip install -r requirements.txt

Start Docker services

bashdocker-compose up -d
🧪 Running Tests Locally
Run All Tests
bashpytest -v
Run Tests by Category
bash# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v
Run Tests with Coverage
bashpytest --cov=app --cov-report=html
View coverage report: open htmlcov/index.html
📊 Test Results

Total Tests: 43
Coverage: 93%
Unit Tests: 30 (password hashing, schema validation)
Integration Tests: 10 (database operations, uniqueness constraints)
E2E Tests: 3 (browser-based calculator tests)

🐳 Docker Hub
Docker images are automatically built and pushed on successful CI/CD pipeline runs:
Repository: pruthul123/assignment10
Pull the latest image:
bashdocker pull pruthul123/assignment10:latest
Run the container:
bashdocker run -p 8000:8000 pruthul123/assignment10:latest
🔐 Key Security Features
Password Hashing

Uses bcrypt algorithm with automatically generated salts
Each password gets a unique hash even if passwords are identical
One-way hashing (cannot reverse-engineer original password)

Input Validation

Email format validation using Pydantic EmailStr
Password strength requirements:

Minimum 8 characters
At least one uppercase letter
At least one lowercase letter
At least one digit



Database Security

Password hashes stored instead of plaintext passwords
Unique constraints prevent duplicate usernames/emails
SQLAlchemy ORM prevents SQL injection attacks

📚 Technologies Used

FastAPI: Modern web framework for building APIs
SQLAlchemy: Python SQL toolkit and ORM
Pydantic: Data validation using Python type annotations
PostgreSQL: Relational database
Bcrypt: Password hashing library
Pytest: Testing framework
Docker: Containerization platform
GitHub Actions: CI/CD automation

🔄 CI/CD Pipeline
The GitHub Actions workflow automatically:

Tests: Runs unit, integration, and E2E tests
Security Scan: Uses Trivy to scan for vulnerabilities
Deploy: Builds and pushes Docker image to Docker Hub

View workflow runs: GitHub Actions
📖 API Documentation
Once the application is running, access interactive API docs:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

 Author
Pruthul Patel

GitHub: @Pruthul15
Docker Hub: pruthul123

Course: IS601.855 - Python for Web API Development
Semester: Fall 2025
Institution: New Jersey Institute of Technology