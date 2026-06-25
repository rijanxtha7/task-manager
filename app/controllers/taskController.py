from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection
from app.utils import login_required
from datetime import datetime

def list_tasks():
    """List all tasks for logged-in user"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    user_id = session.get("user_id")
    conn = get_connection()
    if not conn:
        flash("Database connection error.", "danger")
        return render_template("tasks.html", tasks=[])
    
    cursor = conn.cursor()
    try:
        # Get filter parameter
        status_filter = request.args.get("status", "all")
        
        if status_filter == "completed":
            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = %s AND status = 'completed' ORDER BY created_at DESC",
                (user_id,)
            )
        elif status_filter == "pending":
            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = %s AND status = 'pending' ORDER BY created_at DESC",
                (user_id,)
            )
        else:
            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
        
        tasks = cursor.fetchall()
        return render_template("tasks.html", tasks=tasks, current_filter=status_filter)
    
    except Exception as e:
        flash("Error fetching tasks.", "danger")
        return render_template("tasks.html", tasks=[])
    finally:
        cursor.close()
        conn.close()

def create_task():
    """Create a new task"""
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        user_id = session.get("user_id")
        
        # Validation
        if not title:
            flash("Task title is required.", "danger")
            return render_template("create_task.html")
        
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("create_task.html")
        
        conn = get_connection()
        if not conn:
            flash("Database connection error.", "danger")
            return render_template("create_task.html")
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description, status) VALUES (%s, %s, %s, %s)",
                (user_id, title, description, "pending")
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
    """Edit an existing task"""
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
        
        # Validation
        if not title:
            flash("Task title is required.", "danger")
            return render_template("edit_task.html", task=task)
        
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("edit_task.html", task=task)
        
        try:
            cursor.execute(
                "UPDATE tasks SET title=%s, description=%s, updated_at=NOW() WHERE id=%s",
                (title, description, task_id)
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