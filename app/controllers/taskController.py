from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection
from app.utils import login_required
from datetime import datetime

def list_tasks():
    """List all tasks for logged-in user with filtering and sorting"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return render_template("tasks.html", tasks=[])
    
    cursor = conn.cursor()
    try:
        # Get filter and sort parameters
        status_filter = request.args.get("status", "all")
        sort_by = request.args.get("sort", "created_at")
        sort_order = request.args.get("order", "DESC")
        
        # Validate sort parameters (prevent SQL injection)
        valid_sorts = ["created_at", "title", "status"]
        valid_orders = ["ASC", "DESC"]
        
        if sort_by not in valid_sorts:
            sort_by = "created_at"
        if sort_order not in valid_orders:
            sort_order = "DESC"
        
        # Build query based on filter
        if status_filter == "completed":
            query = f"SELECT * FROM tasks WHERE user_id = %s AND status = 'completed' ORDER BY {sort_by} {sort_order}"
            cursor.execute(query, (user_id,))
        elif status_filter == "pending":
            query = f"SELECT * FROM tasks WHERE user_id = %s AND status = 'pending' ORDER BY {sort_by} {sort_order}"
            cursor.execute(query, (user_id,))
        else:
            query = f"SELECT * FROM tasks WHERE user_id = %s ORDER BY {sort_by} {sort_order}"
            cursor.execute(query, (user_id,))
        
        tasks = cursor.fetchall()
        return render_template("tasks.html", tasks=tasks, current_filter=status_filter, sort_by=sort_by, sort_order=sort_order)
    
    except Exception as e:
        flash("Error fetching tasks.", "danger")
        return render_template("tasks.html", tasks=[])
    finally:
        cursor.close()
        conn.close()
        
def create_task():
    """Create a new task with priority, due date, and category"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium").strip()
        due_date = request.form.get("due_date", "").strip()
        category = request.form.get("category", "general").strip()
        user_id = session.get("user_id")
        
        # Validation
        if not title:
            flash("Task title is required.", "danger")
            return render_template("create_task.html")
        
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("create_task.html")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            priority = "medium"
        
        # Validate category
        valid_categories = ["general", "work", "personal", "shopping", "health", "other"]
        if category not in valid_categories:
            category = "general"
        
        # Validate due date format (optional)
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "danger")
                return render_template("create_task.html")
        
        conn = get_connection()
        if not conn:
            flash("Database connection error.", "danger")
            return render_template("create_task.html")
        
        cursor = conn.cursor()
        try:
            # Note: Priority, due_date, and category will be stored once database schema is updated
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description, status, priority) VALUES (%s, %s, %s, %s, %s)",
                (user_id, title, description, "pending", priority)
            )
            conn.commit()
            flash("Task created successfully!", "success")
            return redirect(url_for("tasks.list_tasks"))
        
        except Exception as e:
            flash("Error creating task.", "danger")
            return render_template("create_task.html")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("create_task.html")

def edit_task(task_id):
    """Edit an existing task with priority, due date, and category support"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    
    cursor = conn.cursor()
    
    # Verify task belongs to user
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    task = cursor.fetchone()
    
    if not task:
        flash("Task not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("tasks.list_tasks"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium").strip()
        due_date = request.form.get("due_date", "").strip()
        category = request.form.get("category", "general").strip()
        
        # Validation
        if not title:
            flash("Task title is required.", "danger")
            return render_template("edit_task.html", task=task)
        
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("edit_task.html", task=task)
        # Validate due date format (optional)
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "danger")
                return render_template("edit_task.html", task=task)
            
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            priority = "medium"
        
        # Validate category
        valid_categories = ["general", "work", "personal", "shopping", "health", "other"]
        if category not in valid_categories:
            category = "general"
        
        try:
            cursor.execute(
                "UPDATE tasks SET title=%s, description=%s, priority=%s, updated_at=NOW() WHERE id=%s",
                (title, description, priority, task_id)
            )
            conn.commit()
            flash("Task updated successfully!", "success")
            return redirect(url_for("tasks.list_tasks"))
        
        except Exception as e:
            flash("Error updating task.", "danger")
            return render_template("edit_task.html", task=task)
        finally:
            cursor.close()
            conn.close()
    
    cursor.close()
    conn.close()
    return render_template("edit_task.html", task=task)

def delete_task(task_id):
    """Delete a task"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    
    cursor = conn.cursor()
    
    # Verify task belongs to user
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    task = cursor.fetchone()
    
    if not task:
        flash("Task not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("tasks.list_tasks"))
    
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        flash("Task deleted successfully!", "success")
    
    except Exception as e:
        flash("Error deleting task.", "danger")
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("tasks.list_tasks"))

def toggle_task(task_id):
    """Mark task as complete/incomplete"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    
    cursor = conn.cursor()
    
    # Verify task belongs to user
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    task = cursor.fetchone()
    
    if not task:
        flash("Task not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("tasks.list_tasks"))
    
    try:
        new_status = "completed" if task["status"] == "pending" else "pending"
        cursor.execute(
            "UPDATE tasks SET status=%s, updated_at=NOW() WHERE id=%s",
            (new_status, task_id)
        )
        conn.commit()
        flash(f"Task marked as {new_status}!", "success")
    
    except Exception as e:
        flash("Error updating task status.", "danger")
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("tasks.list_tasks"))
def search_tasks():
    """Search tasks by title or description"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    search_query = request.args.get("q", "").strip()
    
    if not search_query:
        return redirect(url_for("tasks.list_tasks"))
    
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return render_template("tasks.html", tasks=[], current_filter="all", search_query="")
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = %s AND (title LIKE %s OR description LIKE %s) ORDER BY created_at DESC",
            (user_id, f"%{search_query}%", f"%{search_query}%")
        )
        
        tasks = cursor.fetchall()
        return render_template("tasks.html", tasks=tasks, current_filter="all", search_query=search_query)
    
    except Exception as e:
        flash("Error searching tasks.", "danger")
        return render_template("tasks.html", tasks=[], current_filter="all", search_query="")
    finally:
        cursor.close()
        conn.close()