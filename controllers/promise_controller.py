import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Promise, PromiseUpdate, Politician
from controllers.auth_controller import login_required, admin_required, current_user

promise_bp = Blueprint("promise", __name__)

VALID_STATUSES = {"Has Begun", "On Process", "No update"}

def is_valid_politician_id(pid: str) -> bool:
    return bool(re.fullmatch(r"[1-9][0-9]{7}", pid))

@promise_bp.get("/")
@login_required
def home():
    return redirect(url_for("promise.list_promises"))

@promise_bp.get("/promises")
@login_required
def list_promises():
    sort = request.args.get("sort", "newest")

    if sort == "oldest":
        promises = Promise.query.order_by(Promise.date_of_announcement.asc()).all()
    else:
        sort = "newest"
        promises = Promise.query.order_by(Promise.date_of_announcement.desc()).all()

    return render_template("promises_list.html", promises=promises, user=current_user(), sort=sort)


@promise_bp.get("/promises/<int:promise_id>")
@login_required
def promise_detail(promise_id: int):
    p = Promise.query.get_or_404(promise_id)
    updates = PromiseUpdate.query.filter_by(promise_id=promise_id).order_by(PromiseUpdate.date_of_update.desc()).all()
    return render_template("promise_detail.html", promise=p, updates=updates, user=current_user())

@promise_bp.get("/promises/<int:promise_id>/updates")
@login_required
def promise_updates_page(promise_id: int):
    p = Promise.query.get_or_404(promise_id)
    updates = PromiseUpdate.query.filter_by(promise_id=promise_id).order_by(PromiseUpdate.date_of_update.desc()).all()
    return render_template("promise_updates.html", promise=p, updates=updates, user=current_user())

@promise_bp.post("/promises/<int:promise_id>/updates")
@admin_required
def add_promise_update(promise_id: int):
    p = Promise.query.get_or_404(promise_id)

    if p.promise_status == "No update":
        flash("This promise status is 'No update' and cannot be updated further.")
        return redirect(url_for("promise.promise_updates_page", promise_id=promise_id))

    date_str = request.form.get("date_of_update", "").strip()
    details = request.form.get("progress_details", "").strip()

    if not date_str or not details:
        flash("Date of update and progress details are required.")
        return redirect(url_for("promise.promise_updates_page", promise_id=promise_id))

    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format. Use YYYY-MM-DD.")
        return redirect(url_for("promise.promise_updates_page", promise_id=promise_id))

    upd = PromiseUpdate(promise_id=promise_id, date_of_update=d, progress_details=details)
    db.session.add(upd)
    db.session.commit()

    flash("Update added.")
    return redirect(url_for("promise.promise_updates_page", promise_id=promise_id))
