from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Client Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('service', models.CharField(blank=True, max_length=50, verbose_name='Service Required')),
                ('budget', models.CharField(blank=True, max_length=50, verbose_name='Budget Range')),
                ('message', models.TextField(verbose_name='Project Details')),
                ('status', models.CharField(choices=[('new', 'New Lead'), ('contacted', 'Contacted / In Discussion'), ('quoted', 'Proposal / Quote Sent'), ('won', 'Project Won'), ('closed', 'Closed / Archived')], default='new', max_length=30, verbose_name='Status')),
                ('brevo_message_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Brevo Message ID')),
                ('email_sent', models.BooleanField(default=False, verbose_name='Brevo Email Sent')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Received At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'Contact Inquiry',
                'verbose_name_plural': 'Contact Inquiries (Leads)',
                'ordering': ['-created_at'],
            },
        ),
    ]
