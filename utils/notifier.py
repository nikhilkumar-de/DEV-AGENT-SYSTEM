# =============================================================================
# utils/notifier.py — Email notification sender using smtplib (built-in)
# Used by Module 1 to send missing-commit alerts via Gmail SMTP
# =============================================================================

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

logger = logging.getLogger(__name__)


def send_email(subject: str, body: str):
    """
    Send an email alert to all recipients listed in config.EMAIL_RECIPIENTS.
    Uses Gmail SMTP with TLS (port 587).
    """
    message = MIMEMultipart()
    message["From"]    = config.EMAIL_SENDER
    message["To"]      = ", ".join(config.EMAIL_RECIPIENTS)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()                                          # Secure the connection
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)  # Login with app password
            server.sendmail(
                config.EMAIL_SENDER,
                config.EMAIL_RECIPIENTS,
                message.as_string()
            )
        logger.info(f"Email sent to {config.EMAIL_RECIPIENTS} | Subject: {subject}")

    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email: {e}")
