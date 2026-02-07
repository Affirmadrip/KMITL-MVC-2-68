from flask import Flask
from config import Config
from models import db
from controllers.auth_controller import auth_bp
from controllers.promise_controller import promise_bp
from controllers.politician_controller import politician_bp
from controllers.campaign_controller import campaign_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(promise_bp)
    app.register_blueprint(politician_bp)
    app.register_blueprint(campaign_bp)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
