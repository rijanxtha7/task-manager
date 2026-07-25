import pytest
from app import create_app

@pytest.fixture
def app():
    """Create test Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

# ─── HOME PAGE ───────────────────────────────
def test_home_page_loads(client):
    """Test home page returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_home_page_contains_taskmanager(client):
    """Test home page contains TaskManager title"""
    response = client.get('/')
    assert b'TaskManager' in response.data

# ─── LOGIN ───────────────────────────────────
def test_login_page_loads(client):
    """Test login page returns 200"""
    response = client.get('/login')
    assert response.status_code == 200

def test_login_page_contains_form(client):
    """Test login page has email and password fields"""
    response = client.get('/login')
    assert b'email' in response.data
    assert b'password' in response.data

def test_login_with_invalid_credentials(client):
    """Test login with wrong credentials shows error"""
    response = client.post('/login', data={
        'email': 'wrong@email.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid email or password' in response.data

def test_login_with_empty_fields(client):
    """Test login with empty fields shows error"""
    response = client.post('/login', data={
        'email': '',
        'password': ''
    }, follow_redirects=True)
    assert b'required' in response.data

# ─── REGISTER ────────────────────────────────
def test_register_page_loads(client):
    """Test register page returns 200"""
    response = client.get('/register')
    assert response.status_code == 200

def test_register_page_contains_form(client):
    """Test register page has required fields"""
    response = client.get('/register')
    assert b'name' in response.data
    assert b'email' in response.data
    assert b'password' in response.data

def test_register_with_short_password(client):
    """Test registration fails with password under 6 chars"""
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'password': '123'
    }, follow_redirects=True)
    assert b'6 characters' in response.data

def test_register_with_empty_fields(client):
    """Test registration fails with empty fields"""
    response = client.post('/register', data={
        'name': '',
        'email': '',
        'password': ''
    }, follow_redirects=True)
    assert b'required' in response.data

def test_register_with_invalid_email(client):
    """Test registration fails with invalid email format"""
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'notanemail',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'valid email' in response.data

# ─── PROTECTED ROUTES ────────────────────────
def test_dashboard_redirects_when_not_logged_in(client):
    """Test dashboard redirects unauthenticated users"""
    response = client.get('/dashboard')
    assert response.status_code == 302

def test_tasks_redirects_when_not_logged_in(client):
    """Test tasks page redirects unauthenticated users"""
    response = client.get('/tasks')
    assert response.status_code == 302

def test_create_task_redirects_when_not_logged_in(client):
    """Test create task redirects unauthenticated users"""
    response = client.get('/tasks/create')
    assert response.status_code == 302

# ─── ERROR PAGES ─────────────────────────────
def test_404_page(client):
    """Test 404 error page loads"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

def test_404_contains_message(client):
    """Test 404 page shows not found message"""
    response = client.get('/nonexistent-page')
    assert b'404' in response.data or b'Not Found' in response.data

# ─── NAVIGATION ──────────────────────────────
def test_home_contains_login_link(client):
    """Test home page has login link"""
    response = client.get('/')
    assert b'Login' in response.data

def test_home_contains_register_link(client):
    """Test home page has register link"""
    response = client.get('/')
    assert b'Register' in response.data