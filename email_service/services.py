import os
import requests
import logging
import html
from datetime import datetime
from urllib.parse import quote_plus
from django.conf import settings

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

SERVICE_LABELS = {
    'api': 'REST API Development',
    'webapp': 'Full Stack Web App',
    'frontend': 'Responsive Frontend',
    'database': 'Database Design',
    'auth': 'Auth & Security',
    'devops': 'Deployment & DevOps',
    'other': 'Custom Web Solution'
}

BUDGET_LABELS = {
    'under15k': 'Under ₹15,000',
    '15k-45k': '₹15,000 – ₹45,000',
    '45k-1l': '₹45,000 – ₹1,00,000',
    'above1l': 'Above ₹1,00,000'
}


def build_notification_html(name, email, service, budget, message):
    """
    Generate an executive, modern dark-themed HTML email template
    for KD Technologies company inbox when a new lead submits the form.
    """
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_message = html.escape(message).replace('\n', '<br>')
    service_label = SERVICE_LABELS.get(service, service) if service else 'General Web Inquiry'
    budget_label = BUDGET_LABELS.get(budget, budget) if budget else 'Not specified'
    time_str = datetime.now().strftime("%d %b %Y • %I:%M %p")
    whatsapp_text = quote_plus(f"Hi {name}, thank you for contacting KD Technologies regarding your {service_label} project!")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>New Lead Inquiry</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f1f5f9; line-height: 1.6;">
  <div style="background-color: #0b0f19; padding: 30px 15px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; margin: 0 auto; background-color: #111827; border-radius: 16px; border: 1px solid #1f293d; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.4);">
      
      <!-- Top Neon Accent Bar -->
      <tr>
        <td style="height: 4px; background: linear-gradient(90deg, #7c3aed 0%, #06b6d4 50%, #f472b6 100%);"></td>
      </tr>

      <!-- Header Section -->
      <tr>
        <td style="padding: 32px 30px 24px 30px; background: #111827; border-bottom: 1px solid #1f293d;">
          <table width="100%" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td>
                <span style="display: inline-block; padding: 5px 12px; background: rgba(124, 58, 237, 0.2); border: 1px solid #7c3aed; border-radius: 50px; color: #c4b5fd; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;">
                  ⚡ New Client Inquiry
                </span>
                <h1 style="margin: 14px 0 6px 0; font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                  New Lead: {safe_name}
                </h1>
                <p style="margin: 0; font-size: 13px; color: #94a3b8;">
                  Received through KD Technologies Website &bull; {time_str}
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- Lead Details Grid -->
      <tr>
        <td style="padding: 28px 30px 10px 30px;">
          <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 22px;">
            <tr>
              <td width="48%" style="background: #1e293b; padding: 16px; border-radius: 12px; border: 1px solid #334155; vertical-align: top;">
                <span style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">👤 Client Name</span>
                <div style="font-size: 16px; font-weight: 700; color: #ffffff; margin-top: 4px;">{safe_name}</div>
              </td>
              <td width="4%"></td>
              <td width="48%" style="background: #1e293b; padding: 16px; border-radius: 12px; border: 1px solid #334155; vertical-align: top;">
                <span style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">✉️ Email Address</span>
                <div style="font-size: 15px; font-weight: 600; color: #38bdf8; margin-top: 4px; word-break: break-all;">
                  <a href="mailto:{safe_email}" style="color: #38bdf8; text-decoration: none;">{safe_email}</a>
                </div>
              </td>
            </tr>
          </table>

          <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
            <tr>
              <td width="48%" style="background: #1e293b; padding: 16px; border-radius: 12px; border: 1px solid #334155; vertical-align: top;">
                <span style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">🛠️ Service Requested</span>
                <div style="margin-top: 6px;">
                  <span style="display: inline-block; padding: 4px 10px; background: rgba(6, 182, 212, 0.15); border: 1px solid #06b6d4; border-radius: 6px; font-size: 13px; font-weight: 600; color: #67e8f9;">
                    {service_label}
                  </span>
                </div>
              </td>
              <td width="4%"></td>
              <td width="48%" style="background: #1e293b; padding: 16px; border-radius: 12px; border: 1px solid #334155; vertical-align: top;">
                <span style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">💰 Budget Range</span>
                <div style="margin-top: 6px;">
                  <span style="display: inline-block; padding: 4px 10px; background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius: 6px; font-size: 13px; font-weight: 600; color: #6ee7b7;">
                    {budget_label}
                  </span>
                </div>
              </td>
            </tr>
          </table>

          <!-- Message Card -->
          <div style="background: #0f172a; border-radius: 12px; border: 1px solid #334155; border-left: 4px solid #7c3aed; padding: 20px; margin-bottom: 28px;">
            <div style="font-size: 12px; font-weight: 700; color: #c4b5fd; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 10px;">
              📝 Project Details / Message:
            </div>
            <div style="font-size: 14.5px; color: #e2e8f0; line-height: 1.7; white-space: pre-wrap;">
              {safe_message}
            </div>
          </div>

          <!-- Quick Action Buttons -->
          <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 26px;">
            <tr>
              <td align="center" style="padding-bottom: 10px;">
                <a href="mailto:{safe_email}?subject=Re:%20Your%20Inquiry%20with%20KD%20Technologies%20({quote_plus(service_label)})" style="display: inline-block; background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%); color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-size: 14px; font-weight: 700; box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4); margin-right: 8px;">
                  ✉️ Reply to {safe_name}
                </a>
                <a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="display: inline-block; background: #10b981; color: #ffffff; text-decoration: none; padding: 14px 24px; border-radius: 8px; font-size: 14px; font-weight: 700; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);">
                  💬 Message on WhatsApp
                </a>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td style="padding: 20px 30px; background: #0b0f19; border-top: 1px solid #1f293d; text-align: center;">
          <p style="margin: 0; font-size: 12px; color: #64748b;">
            KD Technologies &bull; Scalable REST APIs & Full Stack Web Apps &bull; Villupuram, Tamil Nadu
          </p>
          <p style="margin: 6px 0 0 0; font-size: 11px; color: #475569;">
            Dispatched via Brevo Transactional Email Engine
          </p>
        </td>
      </tr>
    </table>
  </div>
</body>
</html>"""


def build_confirmation_html(name, service=None, budget=None, message=None):
    """
    Generate an attractive, welcoming, and reassuring HTML confirmation email
    sent to the CUSTOMER after they submit an inquiry.
    """
    safe_name = html.escape(name)
    service_label = SERVICE_LABELS.get(service, service) if service else 'Web Development & APIs'
    budget_label = BUDGET_LABELS.get(budget, budget) if budget else 'Flexible / To be discussed'
    safe_message = (html.escape(message[:200]) + ("..." if len(message or "") > 200 else "")) if message else "Detailed in project scope."

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thank You for Contacting KD Technologies</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6;">
  <div style="background-color: #f1f5f9; padding: 36px 15px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 12px 30px rgba(0,0,0,0.06);">
      
      <!-- Gradient Header Banner -->
      <tr>
        <td style="padding: 40px 32px 32px 32px; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #06b6d4 100%); text-align: left; color: #ffffff;">
          <table width="100%" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td>
                <div style="font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.9; margin-bottom: 8px;">
                  KD TECHNOLOGIES
                </div>
                <h1 style="margin: 0 0 10px 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.25;">
                  We&rsquo;ve Received Your Inquiry! 🚀
                </h1>
                <p style="margin: 0; font-size: 15px; opacity: 0.92; line-height: 1.5;">
                  Thank you for reaching out, <strong>{safe_name}</strong>. We are thrilled to learn more about your project.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- Body Content -->
      <tr>
        <td style="padding: 32px 32px 10px 32px;">
          <p style="font-size: 15px; color: #334155; margin: 0 0 20px 0; line-height: 1.65;">
            Hi <strong>{safe_name}</strong>,
          </p>
          <p style="font-size: 15px; color: #334155; margin: 0 0 24px 0; line-height: 1.65;">
            Thank you for getting in touch with <strong>KD Technologies</strong>. We have received your project details and our team is already reviewing your requirements to provide the best technical solution.
          </p>

          <!-- 3-Step Process / What happens next -->
          <div style="background-color: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; padding: 22px 20px; margin-bottom: 26px;">
            <div style="font-size: 13px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 14px;">
              ⏱️ What Happens Next?
            </div>
            
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 12px;">
              <tr>
                <td width="30" style="vertical-align: top; font-size: 16px;">1️⃣</td>
                <td style="padding-left: 10px; font-size: 14px; color: #334155;">
                  <strong>Requirement Review:</strong> We analyze your scope, tech stack, and roadmap goals.
                </td>
              </tr>
            </table>

            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 12px;">
              <tr>
                <td width="30" style="vertical-align: top; font-size: 16px;">2️⃣</td>
                <td style="padding-left: 10px; font-size: 14px; color: #334155;">
                  <strong>Personal Consultation:</strong> We'll get back to you within <strong>24 business hours</strong> with initial recommendations and an estimate.
                </td>
              </tr>
            </table>

            <table width="100%" border="0" cellpadding="0" cellspacing="0">
              <tr>
                <td width="30" style="vertical-align: top; font-size: 16px;">3️⃣</td>
                <td style="padding-left: 10px; font-size: 14px; color: #334155;">
                  <strong>Kickoff & Build:</strong> Clear milestone timeline, interactive prototype, and development kickoff.
                </td>
              </tr>
            </table>
          </div>

          <!-- Submission Summary Card -->
          <div style="background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 18px 20px; margin-bottom: 26px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <div style="font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">
              📋 Summary of Your Request:
            </div>
            <table width="100%" border="0" cellpadding="6" cellspacing="0" style="font-size: 14px;">
              <tr>
                <td width="35%" style="color: #64748b; font-weight: 600;">Service:</td>
                <td style="color: #0f172a; font-weight: 600;">{service_label}</td>
              </tr>
              <tr>
                <td style="color: #64748b; font-weight: 600;">Budget:</td>
                <td style="color: #0f172a; font-weight: 600;">{budget_label}</td>
              </tr>
              <tr>
                <td style="color: #64748b; font-weight: 600; vertical-align: top;">Your Note:</td>
                <td style="color: #334155; font-style: italic;">&ldquo;{safe_message}&rdquo;</td>
              </tr>
            </table>
          </div>

          <!-- Urgent CTA: WhatsApp -->
          <div style="text-align: center; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 20px; margin-bottom: 28px;">
            <p style="margin: 0 0 12px 0; font-size: 14px; color: #065f46; font-weight: 600;">
              Need an urgent response or want to discuss right away?
            </p>
            <a href="https://wa.me/917397062976?text=Hi%20Prabu,%20I%20just%20submitted%20a%20project%20inquiry%20on%20KD%20Technologies." target="_blank" style="display: inline-block; background-color: #10b981; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 700; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.25);">
              💬 Chat on WhatsApp (+91 73970 62976)
            </a>
          </div>

          <!-- Founder Sign-off -->
          <div style="border-top: 1px solid #f1f5f9; padding-top: 20px; margin-bottom: 24px;">
            <p style="margin: 0; font-size: 14px; color: #64748b;">Warm regards,</p>
            <p style="margin: 4px 0 0 0; font-size: 16px; font-weight: 700; color: #0f172a;">Prabu K</p>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #7c3aed; font-weight: 600;">
              Founder & Lead Full Stack Engineer &bull; KD Technologies
            </p>
            <p style="margin: 4px 0 0 0; font-size: 12px; color: #94a3b8;">
              <a href="mailto:kprabu1512@gmail.com" style="color: #64748b; text-decoration: none;">kprabu1512@gmail.com</a> &bull; 
              <a href="https://linkedin.com/in/prabu-k001" target="_blank" style="color: #64748b; text-decoration: none;">LinkedIn</a> &bull; 
              <a href="https://github.com/Kprabu2001" target="_blank" style="color: #64748b; text-decoration: none;">GitHub</a>
            </p>
          </div>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td style="padding: 20px 32px; background: #f8fafc; border-top: 1px solid #e2e8f0; text-align: center;">
          <p style="margin: 0; font-size: 12px; color: #94a3b8;">
            KD Technologies &bull; Scalable REST APIs, Full Stack Web Apps &bull; Villupuram, Tamil Nadu, India
          </p>
          <p style="margin: 6px 0 0 0; font-size: 11px; color: #cbd5e1;">
            This is an automated confirmation sent because you submitted a request on our website.
          </p>
        </td>
      </tr>
    </table>
  </div>
</body>
</html>"""


def send_contact_email(name, email, service, budget, message):
    """
    Sends transactional emails via Brevo:
    1. Alert to Company inbox (kprabu1512@gmail.com) with lead details & 1-click reply.
    2. Confirmation to Customer (email) with timeline & submission receipt.
    """
    api_key = getattr(settings, 'BREVO_API_KEY', '') or os.getenv('BREVO_API_KEY', '')
    company_email = getattr(settings, 'BREVO_SENDER_EMAIL', '') or os.getenv('BREVO_SENDER_EMAIL', 'kprabu1512@gmail.com')
    company_name = getattr(settings, 'BREVO_SENDER_NAME', 'KD Technologies') or 'KD Technologies'

    if not api_key or api_key == 'your_brevo_api_key_here':
        return {
            'success': False,
            'error': 'Brevo API key is not configured. Please set BREVO_API_KEY in .env'
        }

    if not company_email:
        return {
            'success': False,
            'error': 'Company sender email is not configured. Please set BREVO_SENDER_EMAIL in .env'
        }

    headers = {
        'accept': 'application/json',
        'api-key': api_key,
        'content-type': 'application/json',
    }

    service_label = SERVICE_LABELS.get(service, service) if service else 'General Web Inquiry'
    budget_label = BUDGET_LABELS.get(budget, budget) if budget else 'Not specified'

    # 1. Send Lead Notification to Company inbox (kprabu1512@gmail.com)
    admin_payload = {
        "sender": {
            "name": company_name,
            "email": company_email
        },
        "to": [
            {
                "email": company_email,
                "name": company_name
            }
        ],
        "replyTo": {
            "name": name,
            "email": email
        },
        "subject": f"🔥 New Lead: {service_label} from {name}",
        "htmlContent": build_notification_html(name, email, service, budget, message),
        "textContent": f"New inquiry from {name} ({email})\nService: {service_label}\nBudget: {budget_label}\n\nMessage:\n{message}"
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

        # 2. Send "Get In Touch" Confirmation to Customer (visitor's email)
        send_auto_reply = os.getenv('BREVO_SEND_AUTO_REPLY', 'true').lower() in ('true', '1', 'yes')
        if send_auto_reply:
            try:
                user_payload = {
                    "sender": {
                        "name": company_name,
                        "email": company_email
                    },
                    "to": [
                        {
                            "email": email,
                            "name": name
                        }
                    ],
                    "replyTo": {
                        "name": company_name,
                        "email": company_email
                    },
                    "subject": f"🚀 We've received your project inquiry, {name}! — KD Technologies",
                    "htmlContent": build_confirmation_html(name, service, budget, message),
                    "textContent": f"Hi {name},\n\nThank you for reaching out to KD Technologies! We have received your inquiry.\nOur team will review your project details and get back to you within 24 business hours.\n\nWarm regards,\nPrabu K • KD Technologies"
                }
                requests.post(
                    BREVO_API_URL,
                    headers=headers,
                    json=user_payload,
                    timeout=5
                )
            except Exception as e:
                logger.warning(f"Could not send confirmation email to customer: {e}")

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
