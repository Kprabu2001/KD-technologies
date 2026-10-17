import os
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def build_notification_html(name, email, service, budget, message):
    """Generate modern, responsive HTML email template for inquiry notification."""
    service_label = service or "General Inquiry"
    budget_label = budget or "Not specified"
    
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      margin: 0;
      padding: 0;
      background-color: #f8fafc;
    }}
    .email-wrapper {{
      max-width: 600px;
      margin: 20px auto;
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      border: 1px solid #e2e8f0;
    }}
    .email-header {{
      background: linear-gradient(135deg, #7c3aed, #06b6d4);
      padding: 28px 24px;
      color: #ffffff;
      text-align: left;
    }}
    .email-header h1 {{
      margin: 0;
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }}
    .email-header p {{
      margin: 6px 0 0;
      font-size: 14px;
      opacity: 0.9;
    }}
    .email-body {{
      padding: 28px 24px;
    }}
    .lead-table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }}
    .lead-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid #f1f5f9;
      font-size: 14px;
    }}
    .lead-table td.label {{
      width: 32%;
      font-weight: 600;
      color: #64748b;
      background-color: #f8fafc;
    }}
    .lead-table td.value {{
      color: #0f172a;
      font-weight: 500;
    }}
    .message-box {{
      background: #f8fafc;
      border-left: 4px solid #7c3aed;
      padding: 16px;
      border-radius: 4px;
      margin-top: 10px;
      font-size: 14px;
      color: #334155;
      white-space: pre-wrap;
    }}
    .email-footer {{
      background: #f1f5f9;
      padding: 16px 24px;
      text-align: center;
      font-size: 12px;
      color: #94a3b8;
    }}
    .cta-button {{
      display: inline-block;
      margin-top: 20px;
      background: #7c3aed;
      color: #ffffff !important;
      text-decoration: none;
      padding: 10px 20px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="email-header">
      <h1>🚀 New Inquiry from KD Technologies Website</h1>
      <p>Someone reached out through the contact form.</p>
    </div>
    <div class="email-body">
      <table class="lead-table">
        <tr>
          <td class="label">Client Name</td>
          <td class="value"><strong>{name}</strong></td>
        </tr>
        <tr>
          <td class="label">Client Email</td>
          <td class="value"><a href="mailto:{email}" style="color: #7c3aed; text-decoration: none;">{email}</a></td>
        </tr>
        <tr>
          <td class="label">Service Required</td>
          <td class="value">{service_label}</td>
        </tr>
        <tr>
          <td class="label">Budget Range</td>
          <td class="value">{budget_label}</td>
        </tr>
      </table>

      <strong style="color: #475569; font-size: 14px;">Project Details / Message:</strong>
      <div class="message-box">{message}</div>

      <div style="text-align: center; margin-top: 24px;">
        <a href="mailto:{email}?subject=Re: Your inquiry on KD Technologies" class="cta-button">Reply Directly to {name}</a>
      </div>
    </div>
    <div class="email-footer">
      Sent via KD Technologies Brevo Email Backend &bull; Villupuram, Tamil Nadu, India
    </div>
  </div>
</body>
</html>"""


def build_confirmation_html(name):
    """Generate friendly confirmation email to visitor."""
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      margin: 0;
      padding: 0;
      background-color: #f8fafc;
    }}
    .email-wrapper {{
      max-width: 600px;
      margin: 20px auto;
      background: #ffffff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      border: 1px solid #e2e8f0;
    }}
    .email-header {{
      background: linear-gradient(135deg, #7c3aed, #06b6d4);
      padding: 28px 24px;
      color: #ffffff;
    }}
    .email-header h1 {{
      margin: 0;
      font-size: 22px;
      font-weight: 700;
    }}
    .email-body {{
      padding: 28px 24px;
      font-size: 15px;
      color: #334155;
    }}
    .email-footer {{
      background: #f1f5f9;
      padding: 16px 24px;
      text-align: center;
      font-size: 12px;
      color: #94a3b8;
    }}
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="email-header">
      <h1>Thank You for Contacting KD Technologies!</h1>
    </div>
    <div class="email-body">
      <p>Hi <strong>{name}</strong>,</p>
      <p>Thank you for reaching out! We have received your project details and requirements.</p>
      <p>Our team will review your inquiry and get back to you within <strong>24 business hours</strong> with next steps, questions, or an estimate.</p>
      <p>If you need urgent assistance, you can also reach us directly via WhatsApp at <a href="https://wa.me/917397062976" style="color: #7c3aed; font-weight: 600;">+91 73970 62976</a>.</p>
      <p style="margin-top: 24px;">Warm regards,<br /><strong>Prabu K &bull; KD Technologies</strong></p>
    </div>
    <div class="email-footer">
      KD Technologies &bull; Scalable REST APIs, Full Stack Web Apps &bull; Villupuram, Tamil Nadu
    </div>
  </div>
</body>
</html>"""


def send_contact_email(name, email, service, budget, message):
    """
    Sends an email notification via Brevo's v3 Transactional Email API.
    Optionally sends a confirmation email to the user.
    """
    api_key = getattr(settings, 'BREVO_API_KEY', '') or os.getenv('BREVO_API_KEY', '')
    sender_email = getattr(settings, 'BREVO_SENDER_EMAIL', '') or os.getenv('BREVO_SENDER_EMAIL', '')
    sender_name = getattr(settings, 'BREVO_SENDER_NAME', 'KD Technologies') or os.getenv('BREVO_SENDER_NAME', 'KD Technologies')
    receiver_email = getattr(settings, 'CONTACT_RECEIVER_EMAIL', '') or os.getenv('CONTACT_RECEIVER_EMAIL', '')
    receiver_name = getattr(settings, 'CONTACT_RECEIVER_NAME', 'KD Technologies') or os.getenv('CONTACT_RECEIVER_NAME', 'KD Technologies')

    if not api_key or api_key == 'your_brevo_api_key_here':
        return {
            'success': False,
            'error': 'Brevo API key is not configured. Please set BREVO_API_KEY in .env'
        }

    if not sender_email or sender_email == 'your_verified_sender_email@example.com':
        return {
            'success': False,
            'error': 'Brevo verified sender email is not configured. Please set BREVO_SENDER_EMAIL in .env'
        }

    headers = {
        'accept': 'application/json',
        'api-key': api_key,
        'content-type': 'application/json',
    }

    # 1. Send notification to site owner/team
    admin_payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email
        },
        "to": [
            {
                "email": receiver_email or sender_email,
                "name": receiver_name
            }
        ],
        "replyTo": {
            "name": name,
            "email": email
        },
        "subject": f"🔥 New Lead: {service or 'Project Inquiry'} from {name}",
        "htmlContent": build_notification_html(name, email, service, budget, message),
        "textContent": f"New inquiry from {name} ({email})\nService: {service or 'General Inquiry'}\nBudget: {budget or 'Not specified'}\n\nMessage:\n{message}"
    }

    try:
        response = requests.post(
            BREVO_API_URL,
            headers=headers,
            json=admin_payload,
            timeout=10
        )

        if response.status_code not in (200, 201, 202):
            try:
                err_data = response.json()
                error_msg = err_data.get('message') or str(err_data)
            except Exception:
                error_msg = response.text or f"HTTP {response.status_code}"

            logger.error(f"Brevo API error: {response.status_code} - {error_msg}")
            return {
                'success': False,
                'error': f"Brevo API Error ({response.status_code}): {error_msg}"
            }

        res_data = response.json()
        message_id = res_data.get('messageId', '')

        # 2. Try sending an automatic confirmation to the visitor (non-blocking)
        send_auto_reply = os.getenv('BREVO_SEND_AUTO_REPLY', 'true').lower() in ('true', '1', 'yes')
        if send_auto_reply:
            try:
                user_payload = {
                    "sender": {
                        "name": sender_name,
                        "email": sender_email
                    },
                    "to": [
                        {
                            "email": email,
                            "name": name
                        }
                    ],
                    "subject": "Thank you for contacting KD Technologies! We received your message",
                    "htmlContent": build_confirmation_html(name),
                    "textContent": f"Hi {name},\n\nThank you for reaching out to KD Technologies! We have received your project details and requirements.\nOur team will review your inquiry and get back to you within 24 business hours.\n\nWarm regards,\nPrabu K • KD Technologies"
                }
                requests.post(
                    BREVO_API_URL,
                    headers=headers,
                    json=user_payload,
                    timeout=5
                )
            except Exception as e:
                logger.warning(f"Could not send confirmation email to client: {e}")

        return {
            'success': True,
            'message_id': message_id,
            'message': 'Message sent successfully!'
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while connecting to Brevo: {e}")
        return {
            'success': False,
            'error': f"Failed to connect to email service: {str(e)}"
        }
