from flask import Blueprint, render_template
from models import Campaign
from controllers.auth_controller import login_required, current_user

campaign_bp = Blueprint("campaign", __name__)

@campaign_bp.get("/campaigns")
@login_required
def list_campaigns():
    campaigns = Campaign.query.order_by(Campaign.campaign_id.asc()).all()
    return render_template("campaigns_list.html", campaigns=campaigns, user=current_user())
