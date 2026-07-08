from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection
from app.utils import login_required, admin_required
from werkzeug.security import generate_password_hash, check_password_hash

def home():
    """Home page"""
    return render_template("home.html")

def login():
    """Login route - handles GET and POST requests"""
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        # Validate input
        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")
        
        # Get database connection
        conn = get_connection()
        if not conn:
            flash("Database connection error.", "danger")
            return render_template("login.html")
        
        # Query user by email
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            # Verify password
            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_role"] = user["role"]
                flash("Login successful!", "success")
                return redirect(url_for("auth.dashboard"))
            else:
                flash("Invalid email or password.", "danger")
        
        except Exception as e:
            flash("Login error. Please try again.", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("login.html")

def register():
    """Register route - handles GET and POST requests"""
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        # Validation
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")
        
        if len(name) > 100:
            flash("Name must be under 100 characters.", "danger")
            return render_template("register.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")
        
        # Email format validation
        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html")
        
        # Get database connection
        conn = get_connection()
        if not conn:
            flash("Database connection error.", "danger")
            return render_template("register.html")
        
        # Hash password and save to database
        cursor = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))
        
        except Exception as e:
            if "Duplicate entry" in str(e):
                flash("Email already exists. Please use a different email.", "danger")
            else:
                flash("Registration error. Please try again.", "danger")
            return render_template("register.html")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("register.html")

@login_required
def dashboard():
    """Protected dashboard route - requires login with task statistics"""
    users = []
    task_stats = {"total": 0, "pending": 0, "completed": 0}
    
    user_id = session.get("user_id")
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Get task statistics for logged-in user
            cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE user_id = %s", (user_id,))
            task_stats["total"] = cursor.fetchone()["total"]
            
            cursor.execute("SELECT COUNT(*) as pending FROM tasks WHERE user_id = %s AND status = 'pending'", (user_id,))
            task_stats["pending"] = cursor.fetchone()["pending"]
            
            cursor.execute("SELECT COUNT(*) as completed FROM tasks WHERE user_id = %s AND status = 'completed'", (user_id,))
            task_stats["completed"] = cursor.fetchone()["completed"]
            
            # Show user list if admin
            if session.get("user_role") == "admin":
                cursor.execute("SELECT id, name, email, role, created_at FROM users")
                users = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    return render_template("dashboard.html", users=users, task_stats=task_stats)

def logout():
    """Logout route - clears session"""
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))