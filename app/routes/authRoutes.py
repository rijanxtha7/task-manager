from flask import Blueprint
from app.controllers.authController import (
    login, register, home, logout, dashboard
)

bp = Blueprint('auth', __name__)

# Public routes
bp.route("/")(home)
bp.route("/login", methods=["GET", "POST"])(login)
bp.route("/register", methods=["GET", "POST"])(register)
bp.route("/logout")(logout)

# Protected routes
bp.route("/dashboard")(dashboard)