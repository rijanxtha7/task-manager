# TaskManager

A full-stack web application built with Flask and MySQL for managing personal tasks efficiently.

## Features

## Features

- **User Authentication** - Register, login, and logout securely
- **Session Management** - Secure user sessions with Flask
- **Task Management** - Create, read, update, and delete tasks
- **Task Search** - Search tasks by title or description
- **Task Filtering** - Filter tasks by status (all, pending, completed)
- **Task Sorting** - Sort tasks by date, title, or status
- **Task Priority** - Set task priority (low, medium, high)
- **Task Due Dates** - Set optional due dates for tasks
- **Task Categories** - Organize tasks by category (general, work, personal, shopping, health, other)
- **Task Toggle** - Mark tasks as complete or incomplete
- **Time Tracking** - Start and stop timer to track time spent on each task
- **Time Display** - View today's and total time spent on each task card
- **Admin Dashboard** - Admin users can manage all users
- **User Management** - View and manage all registered users
- **Role-based Access** - Admin and user roles with different permissions
- **Task Statistics** - View total, pending, and completed task counts
- **Password Hashing** - Secure password storage with Werkzeug
- **Input Validation** - Server-side validation for all forms
- **Error Handling** - Custom 403, 404, and 500 error pages
- **Flash Messages** - User feedback for all actions
- **Responsive UI** - Clean and modern interface
- **Environment Variables** - Secure configuration with python-dotenv
- **Parameterized Queries** - Protection against SQL injection

## Technologies Used

- **Backend:** Python, Flask
- **Database:** MySQL with PyMySQL
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Authentication:** Werkzeug password hashing
- **Version Control:** Git & GitHub
- **Environment:** python-dotenv for configuration

## Project Structure
TaskManager/
├── run.py              # Flask entry point
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not committed)
├── .gitignore         # Git ignore rules
└── app/
├── init.py    # Flask app factory
├── database.py    # Database connection
├── utils.py       # Utility decorators
├── controllers/
│   ├── authController.py   # Authentication logic
│   └── taskController.py  # Task management logic
├── routes/
│   ├── authRoutes.py      # Authentication routes
│   └── taskRoutes.py      # Task routes
└── templates/
├── base.html          # Base template
├── home.html          # Home page
├── login.html         # Login page
├── register.html      # Register page
├── dashboard.html     # Dashboard page
├── tasks.html         # Task list page
├── create_task.html   # Create task page
├── edit_task.html     # Edit task page
├── 403.html           # Forbidden error page
├── 404.html           # Not found error page
└── 500.html           # Server error page

## Installation

1. **Clone the repository:**
```bash
[https://github.com/rijanxtha7/task-manager](https://github.com/rijanxtha7/task-manager)
cd task-manager
```

2. **Create virtual environment:**
```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
SECRET_KEY=your-secret-key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=task_manager
DEBUG=True

5. **Create MySQL database:**
```sql
CREATE DATABASE task_manager;
```

6. **Run the application:**
```bash
python run.py
```

7. **Open browser:** `http://127.0.0.1:5000`

## Default Admin Account

- **Email:** admin@taskmanager.com
- **Password:** admin123

## GitHub Repository
https://github.com/rijanxtha7/task-manager.git
