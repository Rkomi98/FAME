"""
Configuration module for the Fame application.

This file defines the configuration settings used by the Flask application,
including secret keys, database connections and mail server details. Most of
these values can be overridden through environment variables. If a value is
not provided via the environment, a sensible default is chosen instead.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class used by the Flask application."""

    # Used by Flask to secure session cookies and other secret data.
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "change-this-secret-key"

    # Configure SQLAlchemy to use a SQLite database by default. A different
    # database can be provided by setting the DATABASE_URL environment variable.
    SQLALCHEMY_DATABASE_URI: str = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Mail configuration. These settings are optional – if MAIL_SERVER is not
    # provided then the send_email function will simply print email contents
    # to stdout instead of attempting to send a real email. To enable real
    # email sending, set MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME
    # and MAIL_PASSWORD appropriately in your environment.
    MAIL_SERVER: str | None = os.environ.get("MAIL_SERVER")
    MAIL_PORT: int = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS: bool = os.environ.get("MAIL_USE_TLS", "false").lower() in [
        "true",
        "1",
        "t",
    ]
    MAIL_USERNAME: str | None = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str | None = os.environ.get("MAIL_PASSWORD")
    # Administrative email address used for notifications. Not currently used
    # but left here for future expansion.
    ADMINS: list[str] = (
        [os.environ.get("ADMIN_EMAIL")] if os.environ.get("ADMIN_EMAIL") else []
    )