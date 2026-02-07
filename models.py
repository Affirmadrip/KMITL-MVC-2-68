from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Politician(db.Model):
    __tablename__ = "politicians"
    politician_id = db.Column(db.String(8), primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)

    promises = db.relationship("Promise", back_populates="politician", cascade="all, delete-orphan")

class Campaign(db.Model):
    __tablename__ = "campaign"
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year_of_campaign = db.Column(db.Integer, nullable=False)
    electoral_district = db.Column(db.String(120), nullable=False)

    politician_id = db.Column(db.String(8), db.ForeignKey("politicians.politician_id"), nullable=False)
    politician = db.relationship("Politician", backref="campaigns")

class Promise(db.Model):
    __tablename__ = "promises"
    promise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    politician_id = db.Column(db.String(8), db.ForeignKey("politicians.politician_id"), nullable=False)
    promise_details = db.Column(db.Text, nullable=False)
    date_of_announcement = db.Column(db.Date, nullable=False, default=date.today)

    promise_status = db.Column(db.String(20), nullable=False) 

    politician = db.relationship("Politician", back_populates="promises")
    updates = db.relationship("PromiseUpdate", back_populates="promise", cascade="all, delete-orphan")

class PromiseUpdate(db.Model):
    __tablename__ = "promiseupdates"
    update_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    promise_id = db.Column(db.Integer, db.ForeignKey("promises.promise_id"), nullable=False)
    date_of_update = db.Column(db.Date, nullable=False)
    progress_details = db.Column(db.Text, nullable=False)

    promise = db.relationship("Promise", back_populates="updates")

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(10), nullable=False)    
