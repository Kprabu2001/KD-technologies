import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from .services import send_contact_email

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def contact_inquiry_view(request):
    """
    Handle contact form submissions and dispatch transactional emails via Brevo.
    Stateless: No database connection or table required.
    """
    # Health check for GET
    if request.method == "GET":
        api_key = getattr(settings, 'BREVO_API_KEY', '') or os.getenv('BREVO_API_KEY', '')
        configured = bool(api_key and api_key != 'your_brevo_api_key_here')
        return JsonResponse({
            "service": "KD Technologies Brevo Email Backend",
            "status": "healthy",
            "brevo_configured": configured
        })

    # Parse POST payload (JSON or Form Data)
    data = {}
    content_type = getattr(request, 'content_type', '') or request.headers.get("Content-Type", "")

    if "application/json" in content_type:
        try:
            raw_body = request.body.decode("utf-8-sig") if request.body else "{}"
            data = json.loads(raw_body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON payload format.",
                "field_errors": {"general": "Invalid JSON payload format."}
            }, status=400)
    else:
        data = request.POST.dict()
        if not data and request.body:
            try:
                data = json.loads(request.body.decode("utf-8-sig"))
            except Exception:
                pass

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    service = str(data.get("service", "")).strip()
    budget = str(data.get("budget", "")).strip()
    message = str(data.get("message", "")).strip()

    # Field validations
    errors = {}
    if not name:
        errors["name"] = "Name is required."
    elif len(name) < 2:
        errors["name"] = "Name must be at least 2 characters."

    if not email:
        errors["email"] = "Email address is required."
    elif not EMAIL_REGEX.match(email):
        errors["email"] = "Please enter a valid email address."

    if not message:
        errors["message"] = "Project details/message are required."
    elif len(message) < 3:
        errors["message"] = "Message must be at least 3 characters."

    if errors:
        error_summary = ", ".join(errors.values())
        return JsonResponse({
            "success": False,
            "error": f"Validation failed: {error_summary}",
            "field_errors": errors
        }, status=400)

    # 1. Send transactional email via Brevo
    result = send_contact_email(
        name=name,
        email=email,
        service=service,
        budget=budget,
        message=message
    )

    brevo_success = bool(result.get("success"))
    brevo_msg_id = result.get("message_id", "")

    if brevo_success:
        return JsonResponse({
            "success": True,
            "message": "Thank you! Your message has been sent successfully. We will be in touch soon.",
            "message_id": brevo_msg_id
        }, status=200)
    else:
        return JsonResponse({
            "success": False,
            "error": result.get("error", "Failed to dispatch email via Brevo.")
        }, status=502)
