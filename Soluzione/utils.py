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

import os
import smtplib
import ssl
from datetime import date, timedelta
from email.mime.text import MIMEText
from typing import List

import requests


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
    if not api_key:
        # Provide a dummy response for local development/testing.
        # The dummy plan includes lunch and dinner for each day of a week.
        dummy = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            dummy.append(
                f"{day} lunch: Example lunch with seasonal vegetables {i+1}."
                f" {day} dinner: Example dinner using local produce {i+1}."
            )
        return "\n".join(dummy)

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        f"?key={api_key}"
    )
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
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Extract the text. Gemini API typically returns a structure like:
            # {'candidates': [{'content': {'parts': [{'text': '...'}]}}]}
            return (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
        else:
            return f"Error from Gemini API: {response.status_code} {response.text}"
    except Exception as exc:
        return f"Exception calling Gemini API: {exc}"


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
    pref_str = ", ".join(preferences) if preferences else "None"
    region_str = region or ""
    # Compose a detailed prompt for the model.
    prompt = (
        "You are a diet planning assistant. Using the following base diet provided "
        f"by a nutritionist: {diet_text}. Create a weekly meal plan starting on "
        f"{start_date.isoformat()} for one person. Include lunch and dinner for each "
        "day of the week (Monday to Sunday). Use seasonal fruits and vegetables "
        f"typical of {region_str}. Avoid these foods: {pref_str}. "
        "Present the plan in a clear format, with each day on a new line in the "
        "format 'Day lunch: ... Day dinner: ...'. After the plan, provide a "
        "separate section labelled 'Shopping List:' followed by a comma-separated list "
        "of all ingredients needed for the week."
    )
    response_text = call_gemini_api(prompt)
    # The response is expected to include a plan and optionally a shopping list.
    # If the shopping list is included, we split on a section header. Otherwise
    # we create a simple shopping list ourselves.
    plan_text = response_text
    shopping_list_text = ""
    if "Shopping List:" in response_text:
        parts = response_text.split("Shopping List:", 1)
        plan_text = parts[0].strip()
        shopping_list_text = parts[1].strip()
    else:
        # Fallback: extract unique ingredient words from the plan. This naive
        # approach simply collects nouns from the text. In real use, the API
        # should return the shopping list directly.
        ingredients = set()
        for line in plan_text.splitlines():
            # Split on commas and spaces
            tokens = [t.strip().lower() for t in line.replace(".", "").split()]
            # Simple heuristic: treat tokens longer than 4 characters as potential ingredients
            for token in tokens:
                if len(token) > 4:
                    ingredients.add(token)
        shopping_list_text = ", ".join(sorted(ingredients))
    return plan_text, shopping_list_text


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