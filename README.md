# KD Technologies — Full-Stack Django Website

A unified Django full-stack web application with Brevo transactional email integration.

---

## 📁 Project Structure

```
KDwebsite/
├── manage.py              # Django management script (run directly from root)
├── core/                  # Django project configuration (renamed from backend/kd_backend)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── email_service/         # App handling Brevo transactional emails
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── templates/             # Frontend HTML templates
│   └── index.html         # Main landing page
├── static/                # Static assets
│   ├── css/style.css      # Dark glassmorphic styles
│   └── js/main.js         # Interactive JS & Brevo form integration
├── .env                   # Brevo API key & environment secrets
├── requirements.txt       # Python dependencies
└── test_brevo.py          # Brevo API test script
```

---

## 🚀 How to Run

### 1. Create & Activate your virtual environment
```powershell
# Create the virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# (Or in Command Prompt: .\venv\Scripts\activate.bat)
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Database Migrations
```powershell
python manage.py migrate
```

### 4. Run the Django Server directly from project root!
```powershell
python manage.py runserver
```

Open **`http://127.0.0.1:8000/`** in your browser!
- The full landing page is served with all styles, animations, and scripts.
- The contact form submits directly to `/api/contact/` and dispatches emails via Brevo to `kprabu152001@gmail.com`.
- Automatic confirmation email is sent to the visitor.

---

## 🧪 Test Brevo API Connection

```powershell
python test_brevo.py
```
