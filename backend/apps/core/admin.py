from django.contrib import admin
from .models import EmailLog, SystemEmailTemplate

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient', 'template_type', 'status', 'created_at', 'sent_at')
    list_filter = ('status', 'template_type')
    search_fields = ('subject', 'recipient', 'error_message')
    readonly_fields = ('created_at', 'sent_at')
    ordering = ('-created_at',)

@admin.register(SystemEmailTemplate)
class SystemEmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'subject', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('event_type', 'subject')
