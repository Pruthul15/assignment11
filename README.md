# IS601 Assignment 11 - Polymorphic Calculation System with Factory Pattern

A FastAPI calculator application implementing polymorphic inheritance with a base `Calculation` class, operation-specific subclasses, factory pattern for object creation, and comprehensive Pydantic schemas for data validation.

[![CI/CD Pipeline](https://github.com/Pruthul15/assignment11/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Pruthul15/assignment11/actions)
[![Docker Hub](https://img.shields.io/docker/pulls/pruthul123/assignment11)](https://hub.docker.com/r/pruthul123/assignment11)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](https://github.com/Pruthul15/assignment11)

## 🎯 Assignment Objectives

This project demonstrates:

- **Polymorphic Design**: Base `Calculation` class with operation-specific subclasses (`AddCalculation`, `SubtractCalculation`, etc.)
- **Factory Pattern**: `CalculationFactory` for dynamic object creation based on operation type
- **Pydantic Schemas**: Type-safe data validation with `CalculationCreate`, `CalculationRead`, and `CalculationUpdate`
- **Comprehensive Testing**: 76 tests achieving 92% code coverage
- **CI/CD Pipeline**: Automated testing, security scanning with Trivy, and Docker Hub deployment

## 🚀 Key Features

### 1. Polymorphic Calculation Model

```python
# Base class with common attributes
class Calculation(Base):
    operation: str
    operand_a: float
    operand_b: float
    result: float
    
# Operation-specific subclasses
class AddCalculation(Calculation):
    __mapper_args__ = {"polymorphic_identity": "add"}

class SubtractCalculation(Calculation):
    __mapper_args__ = {"polymorphic_identity": "subtract"}
```

### 2. Factory Pattern Implementation

```python
class CalculationFactory:
    @staticmethod
    def create(operation: str, a: float, b: float) -> Calculation:
        # Returns appropriate calculation subclass
        return calculation_classes[operation](a, b)
```

### 3. Pydantic Schemas

- `CalculationCreate`: Validates input data for new calculations
- `CalculationRead`: Serializes calculation data for API responses  
- `CalculationUpdate`: Validates partial updates to calculations

## 📁 Project Structure

```
assignment11/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD pipeline (test, security, deploy)
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── calculation.py         # Base Calculation + polymorphic subclasses
│   ├── operations/
│   │   ├── __init__.py
│   │   └── __init__.py            # CalculationFactory implementation
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py                # Base Pydantic schemas
│   │   └── calculation.py         # CalculationCreate, Read, Update schemas
│   └── routers/
│       └── __init__.py            # API route handlers
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_calculation.py        # 29 tests - Calculation model tests
│   ├── test_calculator.py         # 36 tests - Calculator functionality
│   └── test_calculator_memento.py # 12 tests - Memento pattern tests
├── templates/
│   └── index.html                 # Frontend calculator UI
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker container configuration
├── docker-compose.yml             # Multi-container orchestration
├── .env                           # Environment configuration
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
└── REFLECTION.md                  # Assignment reflection document
```

## 🛠️ Technologies Used

- **Backend Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Data Validation**: Pydantic v2
- **Testing Framework**: Pytest with pytest-cov
- **CI/CD**: GitHub Actions
- **Containerization**: Docker & Docker Compose
- **Security Scanning**: Trivy
- **Python Version**: 3.12

## 📦 Installation & Setup

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- Git

### Local Development

**1. Clone the repository**

```bash
git clone https://github.com/Pruthul15/assignment11.git
cd assignment11
```

**2. Create and activate virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

```bash
cp .env.example .env
# Configure DATABASE_URL and other settings in .env
```

**5. Run the application**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**6. Access the application**

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services (FastAPI + PostgreSQL)
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker Hub Image

```bash
# Pull the image
docker pull pruthul123/assignment11:latest

# Run the container
docker run -p 8000:8000 pruthul123/assignment11:latest
```

## 🧪 Running Tests

### Run All Tests with Coverage

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing --cov-fail-under=90

# Run tests with HTML coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Files

```bash
# Test calculation models
pytest tests/test_calculation.py -v

# Test calculator functionality
pytest tests/test_calculator.py -v

# Test memento pattern
pytest tests/test_calculator_memento.py -v
```

### Test Coverage Summary

| Module | Coverage |
|--------|----------|
| app/models/calculation.py | 100% |
| app/operations/__init__.py | 95% |
| app/schemas/calculation.py | 100% |
| **Total** | **92%** |

**Total Tests**: 76 passing

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

### 1. Test Stage

- Sets up Python 3.12 environment
- Installs dependencies
- Runs all 76 tests with coverage reporting
- Fails if coverage < 90%

### 2. Security Stage

- Builds Docker image
- Scans for vulnerabilities using Trivy
- Checks for CRITICAL and HIGH severity issues

### 3. Deploy Stage

- Builds multi-platform Docker image (amd64, arm64)
- Pushes to Docker Hub with tags:
  - `pruthul123/assignment11:latest`
  - `pruthul123/assignment11:<commit-sha>`

**View CI/CD Status**: [GitHub Actions](https://github.com/Pruthul15/assignment11/actions)

## 🐋 Docker Hub

**Repository**: [pruthul123/assignment11](https://hub.docker.com/r/pruthul123/assignment11)

Pull and run the latest image:

```bash
docker pull pruthul123/assignment11:latest
docker run -p 8000:8000 pruthul123/assignment11:latest
```

## 🎨 API Endpoints

### Calculator Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/add` | POST | Add two numbers |
| `/subtract` | POST | Subtract two numbers |
| `/multiply` | POST | Multiply two numbers |
| `/divide` | POST | Divide two numbers |

### Request Format

```json
{
  "a": 10.0,
  "b": 5.0
}
```

### Response Format (Success)

```json
{
  "result": 15.0
}
```

### Response Format (Error)

```json
{
  "error": "Division by zero is not allowed"
}
```

## 🏗️ Design Patterns Implemented

### 1. Polymorphism

- Base `Calculation` class defines common interface
- Subclasses (`AddCalculation`, `SubtractCalculation`, etc.) override behavior
- SQLAlchemy single-table inheritance with `polymorphic_identity`

### 2. Factory Pattern

- `CalculationFactory.create()` encapsulates object creation logic
- Returns appropriate subclass based on operation type
- Eliminates conditional logic in client code

### 3. Strategy Pattern

- Different calculation strategies (add, subtract, multiply, divide)
- Interchangeable at runtime through factory

## 📚 Learning Outcomes Demonstrated

- ✅ **CLO3**: Automated testing with Pytest (76 tests, 92% coverage)
- ✅ **CLO4**: CI/CD with GitHub Actions (test → security → deploy)
- ✅ **CLO6**: Object-oriented programming with polymorphic inheritance
- ✅ **CLO7**: Professional software development practices
- ✅ **CLO9**: Docker containerization and multi-platform builds
- ✅ **CLO11**: SQL database integration with SQLAlchemy ORM
- ✅ **CLO12**: JSON validation with Pydantic schemas




## 👤 Author

**Pruthul Patel**  
IS601 - Web Systems Development  
Assignment 11 - Fall 2025

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- **GitHub Repository**: https://github.com/Pruthul15/assignment11
- **Docker Hub**: https://hub.docker.com/r/pruthul123/assignment11
- **CI/CD Pipeline**: https://github.com/Pruthul15/assignment11/actions

