from flask import Blueprint
from app.controllers.taskController import (
    create_task, list_tasks, edit_task, delete_task, toggle_task, search_tasks
)
from app.utils import login_required

bp_tasks = Blueprint('tasks', __name__)

# Task CRUD routes - all require login
bp_tasks.route("/tasks", methods=["GET"])(login_required(list_tasks))
bp_tasks.route("/tasks/create", methods=["GET", "POST"])(login_required(create_task))
bp_tasks.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])(login_required(edit_task))
bp_tasks.route("/tasks/<int:task_id>/delete", methods=["POST"])(login_required(delete_task))
bp_tasks.route("/tasks/<int:task_id>/toggle", methods=["POST"])(login_required(toggle_task))
bp_tasks.route("/tasks/search", methods=["GET"])(login_required(search_tasks))