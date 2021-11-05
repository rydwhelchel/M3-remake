"""Defines the various models used for the backend database."""
from flask_sqlalchemy import SQLAlchemy
from app_setup import app
from flask_login import UserMixin


db = SQLAlchemy(app)


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Account %r>" % self.username


class FavArtists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    artist_id = db.Column(db.String(120), unique=True, nullable=False)
    artist_name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.artist_name} {self.artist_id}"


db.create_all()
