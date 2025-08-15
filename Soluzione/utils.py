"""
Utility functions for the Fame application.

This module contains helper functions used throughout the application,
including the integration point with Google's Gemini API, routines to
generate weekly meal plans and shopping lists, and a simple email sender.

If certain environment variables are not set, these functions will fall
back to sensible defaults. For example, if no GEMINI_API_KEY is available
the call_gemini_api function will return a mock plan instead of making
an actual network request. Similarly, if mail configuration is missing
send_email will print the message to stdout instead of attempting to send.
"""

from __future__ import annotations

import json
import os
import smtplib
import ssl
from datetime import date, timedelta
from email.mime.text import MIMEText
from typing import List, Dict, Any

import requests


def load_prompt_template() -> str:
    """Load the prompt template from prompt.txt file."""
    try:
        # Get the directory of this utils.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_file = os.path.join(current_dir, "prompt.txt")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback prompt if file not found
        return """Agisci come un nutrizionista esperto. Crea un piano alimentare settimanale in formato JSON con la struttura:
        {"weekly_plan": {"monday": {"lunch": {"title": "...", "description": "...", "focus": "...", "servings": 2}, "dinner": {...}}, ...}, 
        "shopping_list": {"vegetables_fruits": [...], "meat_fish_eggs": [...], ...}, 
        "weekly_summary": {"total_meals": 14, "dietary_focus": "...", "seasonal_highlights": "..."}}"""


def call_gemini_api(prompt: str) -> str:
    """Send a prompt to Google's Gemini API and return its response text.

    The function will attempt to call the generative language API if a
    GEMINI_API_KEY environment variable is present. If the API key is
    missing, a default response is returned for demonstration purposes.

    Args:
        prompt: The prompt text to send to the model.

    Returns:
        The text portion of the model's response. If there was an error or
        no API key is provided, a fallback value is returned.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Debug: Print API call information
    print(f"\n🔍 DEBUG - Gemini API Call")
    print(f"API Key presente: {'✅ Sì' if api_key else '❌ No'}")
    print(f"Lunghezza prompt: {len(prompt)} caratteri")
    print(f"Prime 200 caratteri del prompt: {prompt[:200]}...")
    
    if not api_key:
        print("⚠️  Usando risposta dummy (nessuna API key)")
        # Provide a dummy JSON response for local development/testing.
        dummy_response = {
            "weekly_plan": {
                "monday": {
                    "lunch": {"title": "Insalata di quinoa mediterranea", "description": "Quinoa con pomodorini, olive, feta e basilico", "focus": "Proteico e saziante", "servings": 2},
                    "dinner": {"title": "Salmone al limone con verdure", "description": "Filetto di salmone grigliato con zucchine e carote", "focus": "Omega-3 e antiossidanti", "servings": 3}
                },
                "tuesday": {
                    "lunch": {"title": "Pasta integrale con verdure", "description": "Penne integrali con zucchine, pomodori e basilico", "focus": "Carboidrati complessi", "servings": 2},
                    "dinner": {"title": "Pollo alle erbe con patate", "description": "Petto di pollo marinato con rosmarino e patate al forno", "focus": "Proteine magre", "servings": 3}
                },
                "wednesday": {
                    "lunch": {"title": "Zuppa di legumi", "description": "Minestrone con fagioli, lenticchie e verdure di stagione", "focus": "Fibre e proteine vegetali", "servings": 2},
                    "dinner": {"title": "Pesce bianco in crosta", "description": "Orata con crosta di erbe e verdure grigliate", "focus": "Leggero e digeribile", "servings": 3}
                },
                "thursday": {
                    "lunch": {"title": "Risotto alle verdure", "description": "Risotto integrale con zucca e spinaci", "focus": "Energia a lungo rilascio", "servings": 2},
                    "dinner": {"title": "Tacchino con insalata mista", "description": "Fettine di tacchino con insalata colorata e noci", "focus": "Proteine e vitamine", "servings": 3}
                },
                "friday": {
                    "lunch": {"title": "Wrap di tonno", "description": "Tortilla integrale con tonno, avocado e verdure", "focus": "Pratico e nutriente", "servings": 2},
                    "dinner": {"title": "Pasta con pesto di basilico", "description": "Linguine con pesto fatto in casa e pomodorini", "focus": "Comfort food sano", "servings": 3}
                },
                "saturday": {
                    "lunch": {"title": "Frittata di verdure", "description": "Frittata con zucchine, peperoni e formaggio", "focus": "Proteine e verdure", "servings": 2},
                    "dinner": {"title": "Brasato di manzo", "description": "Brasato con carote, sedano e vino rosso", "focus": "Ricco e sostanzioso", "servings": 3}
                },
                "sunday": {
                    "lunch": {"title": "Insalata di farro", "description": "Farro con verdure grigliate e mozzarella", "focus": "Cereali integrali", "servings": 2},
                    "dinner": {"title": "Branzino al sale", "description": "Branzino intero al sale con patate e rosmarino", "focus": "Tradizionale e saporito", "servings": 3}
                }
            },
            "shopping_list": {
                "vegetables_fruits": ["pomodorini 500g", "zucchine 1kg", "carote 500g", "spinaci 300g", "basilico fresco", "limoni 4 pz"],
                "meat_fish_eggs": ["salmone 600g", "pollo 800g", "orata 500g", "tacchino 400g", "tonno in scatola 2 pz", "manzo per brasato 800g", "branzino 1kg", "uova 6 pz"],
                "dairy_cheese": ["feta 200g", "mozzarella 250g", "parmigiano 150g"],
                "grains_legumes": ["quinoa 300g", "pasta integrale 500g", "fagioli 300g", "lenticchie 200g", "riso integrale 300g", "farro 250g"],
                "pantry_condiments": ["olio extravergine", "aceto balsamico", "olive nere", "noci", "avocado 2 pz", "vino rosso"]
            },
            "weekly_summary": {
                "total_meals": 14,
                "dietary_focus": "Piano equilibrato con varietà di proteine, cereali integrali e verdure di stagione",
                "seasonal_highlights": "Verdure fresche estive, pesce di qualità e legumi nutrienti"
            }
        }
        return json.dumps(dummy_response, ensure_ascii=False, indent=2)

    # Prepare the request payload
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }
    
    # Try different Gemini models in order of preference (newest first)
    models_to_try = [
        "gemini-2.5-flash-lite",      # Gemini 2.5 Flash (sperimentale, più recente)
        "gemini-1.5-flash",          # Gemini 1.5 Flash (stabile, veloce)
        "gemini-1.5-flash-002",      # Versione alternativa di 1.5 Flash
        "gemini-1.5-pro",            # Gemini 1.5 Pro (più potente)
        "gemini-1.5-pro-002",        # Versione alternativa di 1.5 Pro
        "gemini-1.5-pro-001"         # Versione legacy di 1.5 Pro
    ]
    
    for model in models_to_try:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            f"?key={api_key}"
        )
        print(f"🔄 Tentativo con modello: {model}")
        
        try:
            print(f"🌐 Invio richiesta a Gemini API ({model})...")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            print(f"📡 Risposta ricevuta - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Risposta JSON valida ricevuta con {model}")
                
                # Extract the text. Gemini API typically returns a structure like:
                # {'candidates': [{'content': {'parts': [{'text': '...'}]}}]}
                response_text = (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )
                
                print(f"📝 Lunghezza risposta: {len(response_text)} caratteri")
                print(f"📄 Prime 300 caratteri: {response_text[:300]}...")
                
                return response_text
            elif response.status_code == 404:
                print(f"❌ Modello {model} non disponibile, provo il prossimo...")
                continue
            else:
                error_msg = f"Error from Gemini API ({model}): {response.status_code} {response.text}"
                print(f"⚠️ {error_msg}")
                continue
                
        except Exception as exc:
            error_msg = f"Exception calling Gemini API ({model}): {exc}"
            print(f"💥 {error_msg}")
            continue
    
    # If we get here, all Gemini models failed
    print("❌ Tutti i modelli Gemini hanno fallito, provo con OpenAI...")
    return call_openai_api(prompt)


def call_openai_api(prompt: str) -> str:
    """Call OpenAI API as fallback when Gemini fails."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Nessuna API key OpenAI trovata, uso risposta dummy")
        # Return the same dummy response as Gemini fallback
        dummy_response = {
            "weekly_plan": {
                "monday": {
                    "lunch": {"title": "Insalata di quinoa mediterranea", "description": "Quinoa con pomodorini, olive, feta e basilico", "focus": "Proteico e saziante", "servings": 2},
                    "dinner": {"title": "Salmone al limone con verdure", "description": "Filetto di salmone grigliato con zucchine e carote", "focus": "Omega-3 e antiossidanti", "servings": 3}
                },
                "tuesday": {
                    "lunch": {"title": "Pasta integrale con verdure", "description": "Penne integrali con zucchine, pomodori e basilico", "focus": "Carboidrati complessi", "servings": 2},
                    "dinner": {"title": "Pollo alle erbe con patate", "description": "Petto di pollo marinato con rosmarino e patate al forno", "focus": "Proteine magre", "servings": 3}
                },
                "wednesday": {
                    "lunch": {"title": "Zuppa di legumi", "description": "Minestrone con fagioli, lenticchie e verdure di stagione", "focus": "Fibre e proteine vegetali", "servings": 2},
                    "dinner": {"title": "Pesce bianco in crosta", "description": "Orata con crosta di erbe e verdure grigliate", "focus": "Leggero e digeribile", "servings": 3}
                },
                "thursday": {
                    "lunch": {"title": "Risotto alle verdure", "description": "Risotto integrale con zucca e spinaci", "focus": "Energia a lungo rilascio", "servings": 2},
                    "dinner": {"title": "Tacchino con insalata mista", "description": "Fettine di tacchino con insalata colorata e noci", "focus": "Proteine e vitamine", "servings": 3}
                },
                "friday": {
                    "lunch": {"title": "Wrap di tonno", "description": "Tortilla integrale con tonno, avocado e verdure", "focus": "Pratico e nutriente", "servings": 2},
                    "dinner": {"title": "Pasta con pesto di basilico", "description": "Linguine con pesto fatto in casa e pomodorini", "focus": "Comfort food sano", "servings": 3}
                },
                "saturday": {
                    "lunch": {"title": "Frittata di verdure", "description": "Frittata con zucchine, peperoni e formaggio", "focus": "Proteine e verdure", "servings": 2},
                    "dinner": {"title": "Brasato di manzo", "description": "Brasato con carote, sedano e vino rosso", "focus": "Ricco e sostanzioso", "servings": 3}
                },
                "sunday": {
                    "lunch": {"title": "Insalata di farro", "description": "Farro con verdure grigliate e mozzarella", "focus": "Cereali integrali", "servings": 2},
                    "dinner": {"title": "Branzino al sale", "description": "Branzino intero al sale con patate e rosmarino", "focus": "Tradizionale e saporito", "servings": 3}
                }
            },
            "shopping_list": {
                "vegetables_fruits": ["pomodorini 500g", "zucchine 1kg", "carote 500g", "spinaci 300g", "basilico fresco", "limoni 4 pz"],
                "meat_fish_eggs": ["salmone 600g", "pollo 800g", "orata 500g", "tacchino 400g", "tonno in scatola 2 pz", "manzo per brasato 800g", "branzino 1kg", "uova 6 pz"],
                "dairy_cheese": ["feta 200g", "mozzarella 250g", "parmigiano 150g"],
                "grains_legumes": ["quinoa 300g", "pasta integrale 500g", "fagioli 300g", "lenticchie 200g", "riso integrale 300g", "farro 250g"],
                "pantry_condiments": ["olio extravergine", "aceto balsamico", "olive nere", "noci", "avocado 2 pz", "vino rosso"]
            },
            "weekly_summary": {
                "total_meals": 14,
                "dietary_focus": "Piano equilibrato con varietà di proteine, cereali integrali e verdure di stagione",
                "seasonal_highlights": "Verdure fresche estive, pesce di qualità e legumi nutrienti"
            }
        }
        return json.dumps(dummy_response, ensure_ascii=False, indent=2)

    print(f"🔄 Tentativo con OpenAI API...")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        print(f"🌐 Invio richiesta a OpenAI API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📡 Risposta ricevuta - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Risposta JSON valida ricevuta da OpenAI")
            
            response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            print(f"📝 Lunghezza risposta: {len(response_text)} caratteri")
            print(f"📄 Prime 300 caratteri: {response_text[:300]}...")
            
            return response_text
        else:
            error_msg = f"Error from OpenAI API: {response.status_code} {response.text}"
            print(f"❌ {error_msg}")
            return error_msg
    except Exception as exc:
        error_msg = f"Exception calling OpenAI API: {exc}"
        print(f"💥 {error_msg}")
        return error_msg


def generate_weekly_plan(
    diet_text: str,
    preferences: list[str] | None,
    region: str | None,
    start_date: date,
) -> tuple[str, str]:
    """Generate a weekly meal plan and shopping list using the Gemini API.

    The prompt will instruct the model to consider the provided diet,
    disliked foods and region to tailor the meal suggestions. Both lunch and
    dinner will be generated for each day of the week. The function returns
    a tuple containing the plan text and a shopping list text.

    Args:
        diet_text: The raw diet provided by the user's nutritionist.
        preferences: A list of foods the user wants to avoid.
        region: The user's region used to select seasonal produce.
        start_date: The Monday date representing the start of the week.

    Returns:
        A tuple (plan_text, shopping_list_text).
    """
    # Load the prompt template
    prompt_template = load_prompt_template()
    
    # Prepare context variables
    pref_str = ", ".join(preferences) if preferences else "Nessuna preferenza specificata"
    region_str = region or "Italia"
    
    # Compose the detailed prompt with context
    context_prompt = f"""
DIETA BASE FORNITA DAL NUTRIZIONISTA:
{diet_text}

PREFERENZE ALIMENTARI (da evitare):
{pref_str}

REGIONE GEOGRAFICA:
{region_str}

DATA DI INIZIO SETTIMANA:
{start_date.isoformat()} (Lunedì)

{prompt_template}
"""
    
    # Call Gemini API
    response_text = call_gemini_api(context_prompt)
    
    # Try to parse JSON response
    try:
        # Clean the response in case there's extra text
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        plan_data = json.loads(response_text)
        
        # Format the plan text
        plan_text = format_weekly_plan(plan_data.get("weekly_plan", {}))
        
        # Format the shopping list
        shopping_list_text = format_shopping_list(plan_data.get("shopping_list", {}))
        
        return plan_text, shopping_list_text
        
    except json.JSONDecodeError:
        # Fallback: treat as plain text (old format)
        plan_text = response_text
        shopping_list_text = ""
        if "Shopping List:" in response_text:
            parts = response_text.split("Shopping List:", 1)
            plan_text = parts[0].strip()
            shopping_list_text = parts[1].strip()
        else:
            # Simple fallback shopping list
            shopping_list_text = "Lista della spesa non disponibile - utilizzare il piano per creare manualmente"
        
        return plan_text, shopping_list_text


def format_weekly_plan(weekly_plan: Dict[str, Any]) -> str:
    """Format the weekly plan data into readable text."""
    if not weekly_plan:
        return "Piano settimanale non disponibile"
    
    days_map = {
        "monday": "Lunedì",
        "tuesday": "Martedì", 
        "wednesday": "Mercoledì",
        "thursday": "Giovedì",
        "friday": "Venerdì",
        "saturday": "Sabato",
        "sunday": "Domenica"
    }
    
    formatted_lines = []
    
    for day_en, day_it in days_map.items():
        if day_en in weekly_plan:
            day_data = weekly_plan[day_en]
            formatted_lines.append(f"\n🗓️ **{day_it.upper()}**")
            
            if "lunch" in day_data:
                lunch = day_data["lunch"]
                formatted_lines.append(f"🥗 **Pranzo:** {lunch.get('title', 'N/A')}")
                formatted_lines.append(f"   📝 {lunch.get('description', 'N/A')}")
                formatted_lines.append(f"   🎯 {lunch.get('focus', 'N/A')} • {lunch.get('servings', 2)} porzioni")
            
            if "dinner" in day_data:
                dinner = day_data["dinner"]
                formatted_lines.append(f"🍽️ **Cena:** {dinner.get('title', 'N/A')}")
                formatted_lines.append(f"   📝 {dinner.get('description', 'N/A')}")
                formatted_lines.append(f"   🎯 {dinner.get('focus', 'N/A')} • {dinner.get('servings', 3)} porzioni")
    
    return "\n".join(formatted_lines)


def format_shopping_list(shopping_list: Dict[str, List[str]]) -> str:
    """Format the shopping list data into readable HTML text."""
    if not shopping_list:
        return "<p class='text-muted'>Lista della spesa non disponibile</p>"
    
    categories_map = {
        "vegetables_fruits": {"name": "VERDURA E FRUTTA", "icon": "🥬", "color": "#28a745"},
        "meat_fish_eggs": {"name": "CARNE, PESCE E UOVA", "icon": "🥩", "color": "#dc3545"}, 
        "dairy_cheese": {"name": "FORMAGGI E LATTICINI", "icon": "🧀", "color": "#ffc107"},
        "grains_legumes": {"name": "CEREALI E LEGUMI", "icon": "🌾", "color": "#fd7e14"},
        "pantry_condiments": {"name": "DISPENSA E CONDIMENTI", "icon": "🫙", "color": "#6f42c1"}
    }
    
    formatted_sections = []
    
    for category, items in shopping_list.items():
        if category in categories_map and items:
            cat_info = categories_map[category]
            
            # Crea la sezione HTML senza spazi extra
            section_html = f"""<div class="shopping-category mb-4">
                <h6 class="category-header" style="color: {cat_info['color']};">
                    <span class="category-icon">{cat_info['icon']}</span>
                    {cat_info['name']}
                    <span class="badge bg-light text-dark ms-2">{len(items)}</span>
                </h6>
                <div class="category-items">"""
            
            for item in items:
                section_html += f"""
                    <div class="shopping-item">
                        <span class="item-bullet" style="color: {cat_info['color']};">•</span>
                        <span class="item-text">{item}</span>
                    </div>"""
            
            section_html += """
                </div>
            </div>"""
            
            formatted_sections.append(section_html)
    
    return "".join(formatted_sections)


def send_email(to_address: str, subject: str, body: str) -> None:
    """Send an email using SMTP or print the message if mail is not configured.

    The function reads SMTP configuration from environment variables. If a
    mail server is configured (MAIL_SERVER environment variable is set), it
    constructs and sends an email. Otherwise, it prints the email contents.

    Args:
        to_address: Recipient's email address.
        subject: The subject line of the email.
        body: The plain text body of the email.
    """
    mail_server = os.getenv("MAIL_SERVER")
    if not mail_server:
        print("--- Email Output ---")
        print(f"To: {to_address}")
        print(f"Subject: {subject}")
        print(body)
        print("--------------------")
        return
    mail_port = int(os.getenv("MAIL_PORT", 25))
    mail_use_tls = os.getenv("MAIL_USE_TLS", "false").lower() in ["true", "1", "t"]
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = mail_username or "no-reply@example.com"
    message["To"] = to_address

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(mail_server, mail_port) as server:
            if mail_use_tls:
                server.starttls(context=context)
            if mail_username and mail_password:
                server.login(mail_username, mail_password)
            server.sendmail(message["From"], [to_address], message.as_string())
    except Exception as exc:
        print(f"Failed to send email: {exc}")