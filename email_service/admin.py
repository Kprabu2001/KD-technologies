from django.contrib import admin
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'budget', 'status', 'email_sent', 'created_at')
    list_filter = ('status', 'email_sent', 'service', 'created_at')
    search_fields = ('name', 'email', 'message', 'brevo_message_id')
    readonly_fields = ('brevo_message_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    fieldsets = (
        ("Client Details", {
            "fields": ("name", "email", "service", "budget", "message")
        }),
        ("Lead Status & Actions", {
            "fields": ("status",)
        }),
        ("Brevo Email Dispatch Details", {
            "fields": ("email_sent", "brevo_message_id", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
