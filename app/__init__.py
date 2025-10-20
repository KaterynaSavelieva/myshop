# app/__init__.py
import os
from functools import wraps
from flask import Flask, request, Response

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-me")

DASH_USER = os.getenv("DASH_USER", "viewer")
DASH_PASS = os.getenv("DASH_PASS", "viewer123")

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == DASH_USER and auth.password == DASH_PASS):
            return Response("Auth required", 401, {"WWW-Authenticate": 'Basic realm="Dashboard"'})
        return f(*args, **kwargs)
    return wrapper

# Зареєструй твій blueprint
from app.routes import bp as main_bp  # noqa: E402
app.register_blueprint(main_bp)
