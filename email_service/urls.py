from django.urls import path
from .views import contact_inquiry_view

urlpatterns = [
    path('contact/', contact_inquiry_view, name='contact_inquiry'),
]
