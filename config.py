import os
from dotenv import load_dotenv

load_dotenv()

# Secret key for sessions
SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-in-production")

# MySQL Database Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "task_manager")

# Flask Configuration
DEBUG = os.getenv("DEBUG", True)