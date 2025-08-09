"""
Main application file for the Fame web app.

This module creates and configures the Flask application, defines all
routes for user interaction and ties together the database models and
utility functions. Users can register, log in, upload their diets, set
preferences, generate weekly meal plans using the Gemini API and view the
resulting plans. A weekly shopping list is emailed (or printed) when a
plan is generated.
"""

from __future__ import annotations

import os
from datetime import date, timedelta
from io import TextIOWrapper

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Diet, Plan, Preference
from utils import generate_weekly_plan, send_email


def create_app() -> Flask:
    """Factory to create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Setup Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))

    # Create database tables at startup if they don't exist
    @app.before_first_request
    def create_tables() -> None:
        db.create_all()

    # Home page: shows summary or login/register prompts
    @app.route("/")
    def index() -> str:
        if not current_user.is_authenticated:
            return render_template("index.html")
        # Show latest diet and plan summaries on dashboard
        latest_diet = (
            Diet.query.filter_by(user_id=current_user.id)
            .order_by(Diet.uploaded_at.desc())
            .first()
        )
        latest_plan = (
            Plan.query.filter_by(user_id=current_user.id)
            .order_by(Plan.created_at.desc())
            .first()
        )
        return render_template(
            "dashboard.html",
            latest_diet=latest_diet,
            latest_plan=latest_plan,
        )

    # User registration
    @app.route("/register", methods=["GET", "POST"])
    def register() -> str:
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            region = request.form.get("region", "").strip()
            if not username or not email or not password:
                flash("Please fill out all required fields.")
            elif User.query.filter_by(username=username).first():
                flash("Username already exists.")
            elif User.query.filter_by(email=email).first():
                flash("Email already registered.")
            else:
                hashed = generate_password_hash(password)
                new_user = User(
                    username=username,
                    email=email,
                    password=hashed,
                    region=region or None,
                )
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful! Please log in.")
                return redirect(url_for("login"))
        return render_template("register.html")

    # User login
    @app.route("/login", methods=["GET", "POST"])
    def login() -> str:
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("index"))
            flash("Invalid username or password.")
        return render_template("login.html")

    # Logout
    @app.route("/logout")
    @login_required
    def logout() -> str:
        logout_user()
        return redirect(url_for("index"))

    # Upload diet
    @app.route("/upload_diet", methods=["GET", "POST"])
    @login_required
    def upload_diet() -> str:
        if request.method == "POST":
            file = request.files.get("diet_file")
            if not file or file.filename == "":
                flash("No file selected.")
            else:
                # Read file content as text. Assume UTF-8 encoding.
                text = file.read().decode(errors="ignore")
                diet = Diet(user_id=current_user.id, content=text)
                db.session.add(diet)
                db.session.commit()
                flash("Diet uploaded successfully.")
                return redirect(url_for("view_diet"))
        return render_template("upload_diet.html")

    # View diet
    @app.route("/diet")
    @login_required
    def view_diet() -> str:
        diet = (
            Diet.query.filter_by(user_id=current_user.id)
            .order_by(Diet.uploaded_at.desc())
            .first()
        )
        return render_template("diet.html", diet=diet)

    # Preferences
    @app.route("/preferences", methods=["GET", "POST"])
    @login_required
    def preferences() -> str:
        pref = Preference.query.filter_by(user_id=current_user.id).first()
        if request.method == "POST":
            disliked = request.form.get("disliked", "").strip()
            if pref:
                pref.disliked = disliked
            else:
                pref = Preference(user_id=current_user.id, disliked=disliked)
                db.session.add(pref)
            db.session.commit()
            flash("Preferences updated.")
        return render_template("preferences.html", preference=pref)

    # Generate plan
    @app.route("/generate_plan", methods=["POST"])
    @login_required
    def generate_plan() -> str:
        # Get latest diet
        diet = (
            Diet.query.filter_by(user_id=current_user.id)
            .order_by(Diet.uploaded_at.desc())
            .first()
        )
        if not diet:
            flash("Please upload your diet before generating a plan.")
            return redirect(url_for("index"))
        # Determine start date: next Monday
        today = date.today()
        days_ahead = -today.weekday() + 7
        if days_ahead <= 0:
            days_ahead += 7
        start_date = today + timedelta(days=days_ahead)
        # Check if a plan already exists for that week
        existing = Plan.query.filter_by(
            user_id=current_user.id, start_date=start_date
        ).first()
        if existing:
            # Overwrite existing plan
            db.session.delete(existing)
            db.session.commit()
        # Preferences
        pref_record = Preference.query.filter_by(user_id=current_user.id).first()
        preferences_list = []
        if pref_record and pref_record.disliked:
            preferences_list = [p.strip() for p in pref_record.disliked.split(",") if p.strip()]
        # Generate plan via util
        plan_text, shopping_list = generate_weekly_plan(
            diet.content, preferences_list, current_user.region, start_date
        )
        # Save plan
        plan = Plan(
            user_id=current_user.id,
            start_date=start_date,
            content=plan_text,
            shopping_list=shopping_list,
        )
        db.session.add(plan)
        db.session.commit()
        # Send shopping list via email
        send_email(
            current_user.email,
            subject=f"Your Shopping List for week starting {start_date.isoformat()}",
            body=f"Hello {current_user.username},\n\nHere is your meal plan:\n\n{plan_text}\n\nShopping List:\n{shopping_list}\n\nEnjoy your meals!",
        )
        flash("Weekly plan generated and shopping list sent!")
        return redirect(url_for("view_plan"))

    # View plan
    @app.route("/plan")
    @login_required
    def view_plan() -> str:
        plan = (
            Plan.query.filter_by(user_id=current_user.id)
            .order_by(Plan.created_at.desc())
            .first()
        )
        return render_template("plan.html", plan=plan)

    return app


if __name__ == "__main__":
    # When executed directly, run the application.
    flask_app = create_app()
    # Bind to all IPs and use port 5000 by default. Debug mode can be enabled
    # via FLASK_DEBUG environment variable.
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))