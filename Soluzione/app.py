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
from io import TextIOWrapper, BytesIO

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
    jsonify,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from pypdf import PdfReader

from config import Config
from models import db, User, Diet, Plan, Preference
from utils import generate_weekly_plan, send_email, format_weekly_plan
import json

load_dotenv()


def extract_text_from_file(file) -> str:
    """Extract text from uploaded file (supports PDF and text files).
    
    Args:
        file: Flask FileStorage object
        
    Returns:
        Extracted text content as string
    """
    filename = file.filename.lower() if file.filename else ""
    
    if filename.endswith('.pdf'):
        # Handle PDF files
        try:
            file_bytes = file.read()
            pdf_file = BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            
            text_content = []
            for page in reader.pages:
                text_content.append(page.extract_text())
            
            return "\n".join(text_content)
        except Exception as e:
            # Fallback: try to read as text if PDF parsing fails
            file.seek(0)  # Reset file pointer
            return file.read().decode(errors="ignore")
    else:
        # Handle text files
        return file.read().decode(errors="ignore")


def parse_plan_content(content: str) -> dict:
    """Parse plan content to extract structured meal data."""
    try:
        # Try to extract JSON from the original generation if available
        # This is a simplified parser - in a real app you'd want more robust parsing
        structured_plan = {}
        
        days_map = {
            "LUNEDÌ": "monday",
            "MARTEDÌ": "tuesday", 
            "MERCOLEDÌ": "wednesday",
            "GIOVEDÌ": "thursday",
            "VENERDÌ": "friday",
            "SABATO": "saturday",
            "DOMENICA": "sunday"
        }
        
        lines = content.split('\n')
        current_day = None
        current_meal = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if it's a day header
            for day_it, day_en in days_map.items():
                if day_it in line.upper():
                    current_day = day_en
                    structured_plan[current_day] = {}
                    break
            
            # Check if it's a meal
            if current_day and ('**Pranzo:**' in line or '🥗 **Pranzo:**' in line):
                title = line.split('**Pranzo:**')[1].strip() if '**Pranzo:**' in line else line.split('🥗 **Pranzo:**')[1].strip()
                structured_plan[current_day]['lunch'] = {'title': title, 'description': '', 'focus': '', 'servings': 2}
                current_meal = 'lunch'
            elif current_day and ('**Cena:**' in line or '🍽️ **Cena:**' in line):
                title = line.split('**Cena:**')[1].strip() if '**Cena:**' in line else line.split('🍽️ **Cena:**')[1].strip()
                structured_plan[current_day]['dinner'] = {'title': title, 'description': '', 'focus': '', 'servings': 3}
                current_meal = 'dinner'
            elif current_day and current_meal and line.startswith('📝'):
                structured_plan[current_day][current_meal]['description'] = line.replace('📝', '').strip()
            elif current_day and current_meal and line.startswith('🎯'):
                focus_info = line.replace('🎯', '').strip()
                if '•' in focus_info:
                    parts = focus_info.split('•')
                    structured_plan[current_day][current_meal]['focus'] = parts[0].strip()
                    if len(parts) > 1:
                        servings_text = parts[1].strip()
                        if 'porzioni' in servings_text:
                            try:
                                servings = int(servings_text.split()[0])
                                structured_plan[current_day][current_meal]['servings'] = servings
                            except:
                                pass
                else:
                    structured_plan[current_day][current_meal]['focus'] = focus_info
        
        return structured_plan
    except Exception as e:
        print(f"Error parsing plan content: {e}")
        return {}


def generate_preparation_instructions(title: str, description: str) -> str:
    """Generate basic preparation instructions for a meal."""
    # This is a simple implementation - in a real app you might use AI or a database
    instructions = []
    
    if "salmone" in title.lower():
        instructions.extend([
            "1. Preriscalda il forno a 180°C",
            "2. Condisci il salmone con olio, sale e limone", 
            "3. Cuoci per 15-20 minuti",
            "4. Prepara le verdure di contorno"
        ])
    elif "pasta" in title.lower():
        instructions.extend([
            "1. Porta a ebollizione abbondante acqua salata",
            "2. Cuoci la pasta secondo i tempi di cottura",
            "3. Prepara il condimento in padella",
            "4. Manteca la pasta con il condimento"
        ])
    elif "pollo" in title.lower():
        instructions.extend([
            "1. Taglia il pollo a pezzi regolari",
            "2. Marinalo con erbe e spezie per 30 minuti",
            "3. Cuoci in padella o al forno",
            "4. Controlla la cottura interna"
        ])
    elif "insalata" in title.lower():
        instructions.extend([
            "1. Lava e asciuga bene le verdure",
            "2. Taglia gli ingredienti a pezzi uniformi",
            "3. Prepara il condimento a parte",
            "4. Condisci solo prima di servire"
        ])
    else:
        # Generic instructions
        instructions.extend([
            "1. Prepara tutti gli ingredienti necessari",
            "2. Segui la ricetta tradizionale per questo piatto",
            "3. Cuoci rispettando i tempi indicati",
            "4. Servi caldo e gustoso"
        ])
    
    return "\n".join(instructions)


def create_app() -> Flask:
    """Factory to create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Enable CORS for frontend deployment
    CORS(app, origins=["https://yourusername.github.io", "http://localhost:3000", "http://localhost:5000"])
    
    # Add custom template filter for newlines to br tags
    @app.template_filter('nl2br')
    def nl2br(text):
        """Convert newlines to HTML br tags."""
        if not text:
            return text
        return text.replace('\n', '<br>\n')

    # Setup Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))

    # Create database tables at startup if they don't exist
    @app.before_request
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
            api_provider = request.form.get("api_provider", "gemini").strip()
            api_key = request.form.get("api_key", "").strip()
            
            if not username or not email or not password or not api_key:
                flash("Please fill out all required fields including API key.")
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
                    api_provider=api_provider,
                    api_key=api_key,  # In production, this should be encrypted
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
                try:
                    # Extract text from file (supports PDF and text files)
                    text = extract_text_from_file(file)
                    if not text.strip():
                        flash("The uploaded file appears to be empty or could not be read.")
                    else:
                        diet = Diet(user_id=current_user.id, content=text)
                        db.session.add(diet)
                        db.session.commit()
                        flash(f"Diet uploaded successfully from {file.filename}!")
                        return redirect(url_for("view_diet"))
                except Exception as e:
                    flash(f"Error processing file: {str(e)}")
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

            current_user.trains = 'trains' in request.form
            if current_user.trains:
                current_user.training_frequency = request.form.get('training_frequency')
                training_days = request.form.getlist('training_days')
                current_user.training_days = ','.join(training_days)
            else:
                current_user.training_frequency = None
                current_user.training_days = None
            
            db.session.commit()
            flash("Preferences updated.")
        return render_template("preferences.html", preference=pref, user=current_user)

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
        plan_text, shopping_list, raw_json = generate_weekly_plan(
            diet.content,
            preferences_list,
            current_user.region,
            start_date,
            current_user.trains,
            current_user.training_frequency,
            current_user.training_days,
            current_user.api_provider,
            current_user.api_key,
        )
        # Save plan
        plan = Plan(
            user_id=current_user.id,
            start_date=start_date,
            content=plan_text,
            json_content=raw_json,
            shopping_list=shopping_list,
        )
        db.session.add(plan)
        db.session.commit()
        # Send shopping list via email to user's own email
        send_email(
            current_user.email,
            subject=f"Your Shopping List for week starting {start_date.isoformat()}",
            body=f"Hello {current_user.username},\n\nHere is your meal plan:\n\n{plan_text}\n\nShopping List:\n{shopping_list}\n\nEnjoy your meals!",
        )
        flash("Weekly plan generated and shopping list sent to your email!")
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
        
        # Parse plan content to extract structured data
        structured_plan = None
        if plan and plan.json_content:
            try:
                structured_plan = json.loads(plan.json_content).get("weekly_plan")
            except json.JSONDecodeError:
                structured_plan = parse_plan_content(plan.content)
        elif plan and plan.content:
            structured_plan = parse_plan_content(plan.content)
        
        return render_template("plan.html", plan=plan, structured_plan=structured_plan, timedelta=timedelta)
    
    # API endpoint for meal details
    @app.route("/api/meal_details/<day>/<meal_type>")
    @login_required
    def get_meal_details(day: str, meal_type: str) -> dict:
        plan = (
            Plan.query.filter_by(user_id=current_user.id)
            .order_by(Plan.created_at.desc())
            .first()
        )
        
        if not plan:
            return {"error": "No plan found"}, 404
            
        structured_plan = {}
        if plan.json_content:
            try:
                structured_plan = json.loads(plan.json_content).get("weekly_plan", {})
            except json.JSONDecodeError:
                pass # Fallback to parsing content below

        if not structured_plan:
             structured_plan = parse_plan_content(plan.content)

        if not structured_plan or day not in structured_plan:
            return {"error": "Day not found"}, 404
            
        if meal_type not in structured_plan[day]:
            return {"error": "Meal not found"}, 404
            
        meal = structured_plan[day][meal_type]
        
        # Add preparation instructions (dummy for now, could be enhanced)
        meal["preparation"] = generate_preparation_instructions(meal.get("title", ""), meal.get("description", ""))
        
        return meal

    @app.route("/api/delete_meal/<int:plan_id>/<day>/<meal_type>", methods=["DELETE"])
    @login_required
    def delete_meal(plan_id, day, meal_type):
        plan = Plan.query.filter_by(id=plan_id, user_id=current_user.id).first()
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        if not plan.json_content:
            return jsonify({"error": "Cannot modify a plan without structured data"}), 400

        try:
            plan_data = json.loads(plan.json_content)
            weekly_plan = plan_data.get("weekly_plan", {})

            if day in weekly_plan and meal_type in weekly_plan[day]:
                del weekly_plan[day][meal_type]
                if not weekly_plan[day]: # remove day if empty
                    del weekly_plan[day]

                plan_data["weekly_plan"] = weekly_plan
                
                # Update json_content and regenerate text content
                plan.json_content = json.dumps(plan_data, ensure_ascii=False, indent=2)
                plan.content = format_weekly_plan(weekly_plan)
                
                # We will tackle shopping list regeneration later.
                # For now, let's just add a note.
                if "Nota:" not in plan.shopping_list:
                    plan.shopping_list += "\\n\\n---\\n**Nota:** Il piano è stato modificato. La lista della spesa potrebbe non essere più accurata."

                db.session.commit()
                return jsonify({"success": True}), 200
            else:
                return jsonify({"error": "Meal not found in plan"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid plan content format"}), 500


    # Send shopping list to custom email
    @app.route("/send_shopping_list", methods=["POST"])
    @login_required
    def send_shopping_list() -> str:
        email_address = request.form.get("email_address", "").strip()
        if not email_address:
            flash("Please provide an email address.", "error")
            return redirect(url_for("view_plan"))
        
        # Get the latest plan
        plan = (
            Plan.query.filter_by(user_id=current_user.id)
            .order_by(Plan.created_at.desc())
            .first()
        )
        
        if not plan:
            flash("No plan available to send.", "error")
            return redirect(url_for("view_plan"))
        
        # Add email to favorites
        current_user.add_favorite_email(email_address)
        db.session.commit()
        
        # Send email
        send_email(
            email_address,
            subject=f"Shopping List from {current_user.username} - Week starting {plan.start_date.isoformat()}",
            body=f"Hello,\n\n{current_user.username} has shared their shopping list with you:\n\n{plan.shopping_list}\n\nEnjoy your meals!",
        )
        
        flash(f"Shopping list sent to {email_address}!", "success")
        return redirect(url_for("view_plan"))

    # API endpoint to get favorite emails
    @app.route("/api/favorite_emails")
    @login_required
    def get_favorite_emails():
        return jsonify({"emails": current_user.get_favorite_emails()})

    return app


if __name__ == "__main__":
    # When executed directly, run the application.
    flask_app = create_app()
    # Bind to all IPs and use port 5000 by default. Debug mode can be enabled
    # via FLASK_DEBUG environment variable.
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))