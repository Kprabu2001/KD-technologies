from django.db import models


class ContactInquiry(models.Model):
    SERVICE_CHOICES = [
        ('api', 'REST API Development'),
        ('webapp', 'Full Stack Web App'),
        ('frontend', 'Responsive Frontend'),
        ('database', 'Database Design'),
        ('auth', 'Auth & Security'),
        ('devops', 'Deployment & DevOps'),
        ('other', 'Other Inquiry'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted / In Discussion'),
        ('quoted', 'Proposal / Quote Sent'),
        ('won', 'Project Won'),
        ('closed', 'Closed / Archived'),
    ]

    name = models.CharField(max_length=150, verbose_name="Client Name")
    email = models.EmailField(verbose_name="Email Address")
    service = models.CharField(max_length=50, blank=True, verbose_name="Service Required")
    budget = models.CharField(max_length=50, blank=True, verbose_name="Budget Range")
    message = models.TextField(verbose_name="Project Details")

    # Tracking & status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    brevo_message_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Brevo Message ID")
    email_sent = models.BooleanField(default=False, verbose_name="Brevo Email Sent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Received At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries (Leads)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service or 'Inquiry'} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
