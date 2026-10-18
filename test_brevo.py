"""
Test script to verify Brevo API Key and send a test email.
Run with: python test_brevo.py
"""

import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)

api_key = os.getenv('BREVO_API_KEY', '')
sender_email = os.getenv('BREVO_SENDER_EMAIL', 'kprabu1512@gmail.com')
sender_name = os.getenv('BREVO_SENDER_NAME', 'KD Technologies')
receiver_email = os.getenv('CONTACT_RECEIVER_EMAIL', 'kprabu152001@gmail.com')

print("=" * 50)
print("KD Technologies — Brevo API Verification")
print("=" * 50)
print(f"API Key: {api_key[:12]}...{api_key[-6:] if len(api_key) > 18 else ''}")
print(f"Sender: {sender_name} <{sender_email}>")
print(f"Receiver: {receiver_email}")
print("-" * 50)

if not api_key or api_key == 'your_brevo_api_key_here':
    print("❌ Error: BREVO_API_KEY is not configured in .env")
    exit(1)

# Step 1: Check account / API key validity
print("1. Checking Brevo Account with API Key...")
account_url = "https://api.brevo.com/v3/account"
headers = {
    "accept": "application/json",
    "api-key": api_key
}

try:
    acc_res = requests.get(account_url, headers=headers, timeout=10)
    if acc_res.status_code == 200:
        acc_data = acc_res.json()
        print(f"✅ Brevo API Key is VALID!")
        print(f"   Account Email: {acc_data.get('email')}")
        print(f"   Plan: {acc_data.get('plan', [{}])[0].get('type', 'N/A') if acc_data.get('plan') else 'Active'}")
    else:
        print(f"❌ Brevo API Error ({acc_res.status_code}): {acc_res.text}")
        exit(1)
except Exception as e:
    print(f"❌ Network error while connecting to Brevo: {e}")
    exit(1)

# Step 2: Send test transactional email
print("\n2. Sending test transactional email...")
email_url = "https://api.brevo.com/v3/smtp/email"
payload = {
    "sender": {"name": sender_name, "email": sender_email},
    "to": [{"email": receiver_email, "name": "KD Admin"}],
    "subject": "🚀 KD Technologies: Brevo API Integration Test Successful",
    "htmlContent": f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f8fafc; border-radius: 8px;">
            <h2 style="color: #7c3aed;">🎉 Brevo API is working perfectly!</h2>
            <p>Your Django unified email service for <strong>KD Technologies</strong> is now connected and ready to send customer inquiries.</p>
            <p><strong>Configured Sender:</strong> {sender_email}</p>
            <p><strong>Configured Receiver:</strong> {receiver_email}</p>
        </div>
    """,
    "textContent": "KD Technologies Brevo API test successful!"
}

try:
    mail_res = requests.post(email_url, headers={"content-type": "application/json", **headers}, json=payload, timeout=10)
    if mail_res.status_code in (200, 201, 202):
        print(f"✅ Test Email sent successfully! Message ID: {mail_res.json().get('messageId')}")
        print(f"   Check your inbox at {receiver_email}")
    else:
        print(f"⚠️ Email dispatch warning ({mail_res.status_code}): {mail_res.text}")
        print("Note: If error mentions unverified sender, verify your sender email at https://app.brevo.com/senders")
except Exception as e:
    print(f"❌ Failed to send email: {e}")

print("=" * 50)
