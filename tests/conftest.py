"""
Test configuration and fixtures with Faker support.
"""
import pytest
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.database import Base
from app.models.user import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

fake = Faker()


def create_fake_user():
    """Generate fake user data"""
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "TestPassword123"
    }


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(username="testuser", email="test@example.com")
    user.set_password("TestPassword123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def seed_users(db_session):
    """Seed multiple test users"""
    users = []
    for _ in range(3):
        user_data = create_fake_user()
        user = User(username=user_data['username'], email=user_data['email'])
        user.set_password(user_data['password'])
        users.append(user)
        db_session.add(user)
    db_session.commit()
    return users


@contextmanager
def managed_db_session() -> Session:
    """Context manager for manual database sessions"""
    engine = create_engine(TEST_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session error: {e}")
        raise
    finally:
        session.close()


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")


# Playwright fixtures for E2E tests
@pytest.fixture(scope="session")
def browser():
    """Launch browser for E2E tests"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each test"""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def fastapi_server():
    """Start FastAPI server for E2E tests"""
    import subprocess
    import time
    
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # Wait for server to start
    yield
    process.kill()


# ============================================================================
# Playwright Fixtures for E2E Tests
# ============================================================================

import pytest
from playwright.sync_api import sync_playwright
import subprocess
import time


@pytest.fixture(scope="session")
def browser():
    """Launch Chromium browser for E2E tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each E2E test"""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def fastapi_server():
    """Start FastAPI server for E2E tests"""
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Wait for server to start
    yield
    process.kill()
    process.wait()


# ============================================================================
# Playwright Fixtures for E2E Tests
# ============================================================================

import subprocess
import time


@pytest.fixture(scope="session")
def browser():
    """Launch Chromium browser for E2E tests"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each E2E test"""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def fastapi_server():
    """Start FastAPI server for E2E tests"""
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Wait for server to start
    yield
    process.kill()
    process.wait()
