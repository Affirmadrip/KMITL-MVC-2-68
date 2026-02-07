from flask import Blueprint, render_template
from models import Politician, Promise
from controllers.auth_controller import login_required, current_user

politician_bp = Blueprint("politician", __name__)

@politician_bp.get("/politicians")
@login_required
def list_politicians():
    pols = Politician.query.order_by(Politician.name.asc()).all()
    return render_template("politicians_list.html", politicians=pols, user=current_user())

@politician_bp.get("/politicians/<politician_id>")
@login_required
def politician_detail(politician_id: str):
    pol = Politician.query.get_or_404(politician_id)
    promises = Promise.query.filter_by(politician_id=politician_id).order_by(Promise.date_of_announcement.desc()).all()
    return render_template("politician_detail.html", politician=pol, promises=promises, user=current_user())
