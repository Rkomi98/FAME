"""
Unit tests for the utility functions in the Fame application.

These tests verify that the stubbed Gemini API returns a sensible plan when
no API key is provided, that the weekly plan generator returns both plan
and shopping list text, and that the email sender prints messages when
mail settings are not configured. The tests use Python's built‑in
unittest framework so they can run without additional dependencies.
"""

import os
import unittest
from datetime import date
from io import StringIO
import sys

from fame_app.utils import call_gemini_api, generate_weekly_plan, send_email


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Ensure GEMINI_API_KEY is not set to force dummy response
        self.original_api_key = os.environ.pop("GEMINI_API_KEY", None)

    def tearDown(self):
        # Restore any original API key
        if self.original_api_key is not None:
            os.environ["GEMINI_API_KEY"] = self.original_api_key

    def test_call_gemini_api_dummy(self):
        prompt = "Generate a weekly plan"
        response = call_gemini_api(prompt)
        # The dummy response should include seven lines (one per day)
        lines = response.strip().split("\n")
        self.assertEqual(len(lines), 7)
        # Ensure each line contains both lunch and dinner
        for line in lines:
            self.assertIn("lunch", line.lower())
            self.assertIn("dinner", line.lower())

    def test_generate_weekly_plan(self):
        diet_text = "Balanced diet"
        preferences = ["tomatoes"]
        region = "Campania, Italy"
        start_date = date.today()
        plan_text, shopping = generate_weekly_plan(diet_text, preferences, region, start_date)
        self.assertTrue(plan_text)
        self.assertTrue(shopping)
        # The shopping list should be a comma-separated string
        self.assertIn(",", shopping)

    def test_send_email_print(self):
        # Ensure no mail server configured
        original_mail_server = os.environ.pop("MAIL_SERVER", None)
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            send_email("test@example.com", "Subject", "Body text")
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            # Check that email output contains recipients and subject
            self.assertIn("test@example.com", output)
            self.assertIn("Subject", output)
            self.assertIn("Body text", output)
        finally:
            # Restore stdout and environment
            sys.stdout = sys.__stdout__
            if original_mail_server is not None:
                os.environ["MAIL_SERVER"] = original_mail_server


if __name__ == '__main__':
    unittest.main()