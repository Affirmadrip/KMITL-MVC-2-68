from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User

auth_bp = Blueprint("auth", __name__)

def current_user():
    username = session.get("username")
    if not username:
        return None
    return User.query.get(username)

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u:
            return redirect(url_for("auth.login"))
        if u.role != "admin":
            flash("Admin only.")
            return redirect(url_for("promise.list_promises"))
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.get("/login")
def login():
    return render_template("login.html")

@auth_bp.post("/login")
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    u = User.query.get(username)
    if not u or u.password != password:
        flash("Invalid username or password.")
        return redirect(url_for("auth.login"))
    session["username"] = u.username
    return redirect(url_for("promise.list_promises"))

@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
