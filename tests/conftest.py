"""
Test configuration and fixtures with Faker support.
Author: Pruthul Patel
Date: October 18, 2025
"""
import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.database import Base
from app.models.user import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use SQLite for tests (NOT PostgreSQL)
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
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")


# Playwright fixtures for E2E tests
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
    """Start FastAPI server for E2E tests with proper initialization"""
    import subprocess
    import time
    import socket
    
    def is_port_in_use(port):
        """Check if a port is in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    # Kill any existing process on port 8000
    if is_port_in_use(8000):
        try:
            subprocess.run(["fuser", "-k", "8000/tcp"], stderr=subprocess.DEVNULL)
            time.sleep(1)
        except FileNotFoundError:
            # fuser not available on all systems
            pass
    
    # Start the FastAPI server
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to be ready (up to 10 seconds)
    max_wait = 10
    server_ready = False
    for _ in range(max_wait * 2):
        if is_port_in_use(8000):
            time.sleep(0.5)  # Extra time for server to fully initialize
            server_ready = True
            break
        time.sleep(0.5)
    
    if not server_ready:
        process.kill()
        process.wait()
        raise RuntimeError("FastAPI server failed to start within 10 seconds")
    
    logger.info("FastAPI server started successfully on port 8000")
    
    yield
    
    # Cleanup: kill the server
    process.kill()
    process.wait()
    logger.info("FastAPI server stopped")