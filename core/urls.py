from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home_view(request):
    """Serve the KD Technologies frontend landing page."""
    return render(request, 'index.html')

def root_status(request):
    """API health status endpoint."""
    return JsonResponse({
        "app": "KD Technologies Unified Django App",
        "email_service": "Brevo Integration",
        "status": "online",
        "api_endpoint": "/api/contact/"
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('api/status/', root_status, name='root_status'),
    path('admin/', admin.site.urls),
    path('api/', include('email_service.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
