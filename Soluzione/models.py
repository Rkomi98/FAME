"""
Database models for the Fame application.

This module defines the SQLAlchemy models used by the application. Users can
upload diets, specify their preferences and generate weekly plans. Plans
include a weekly meal schedule as well as a shopping list. Each model is
associated with a user via a foreign key.
"""

from datetime import datetime, date

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# The SQLAlchemy database instance is created in this module so that it can
# be imported by any other modules without causing a circular import. The
# actual application will initialise the database in app.py.
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Represents an authenticated user in the Fame application."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Region used to tailor seasonal produce suggestions (e.g. "Campania, Italy").
    region = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships: a user may have many preferences, diets and plans.
    preferences = db.relationship("Preference", backref="user", lazy=True)
    diets = db.relationship("Diet", backref="user", lazy=True)
    plans = db.relationship("Plan", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Preference(db.Model):
    """Stores food dislikes and allergies for a user."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # A comma-separated list of foods the user dislikes or is allergic to.
    disliked = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Preference for User {self.user_id}: {self.disliked}>"


class Diet(db.Model):
    """Represents a diet plan provided by a nutritionist."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Raw content of the diet, typically uploaded as plain text.
    content = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Diet {self.id} for User {self.user_id}>"


class Plan(db.Model):
    """Represents a weekly meal plan generated for a user."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Start date of the plan (Monday). Only one plan per week per user.
    start_date = db.Column(db.Date, nullable=False)
    # Textual representation of the meals for the week.
    content = db.Column(db.Text, nullable=False)
    # Shopping list text generated for the week.
    shopping_list = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<Plan for User {self.user_id} starting {self.start_date.isoformat()}>"
        )