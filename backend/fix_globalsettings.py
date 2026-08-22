import re

with open('apps/core/admin.py', 'r') as f:
    content = f.read()

new_admin_code = """
from django import forms
from unfold.widgets import (
    UnfoldAdminTextInputWidget,
    UnfoldAdminColorInputWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminPasswordInputWidget
)

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = '__all__'
        widgets = {
            'site_name': UnfoldAdminTextInputWidget(attrs={'class': 'font-bold text-xl'}),
            'support_email': UnfoldAdminEmailInputWidget(),
            'site_logo': UnfoldAdminImageFieldWidget(),
            'site_favicon': UnfoldAdminImageFieldWidget(),
            'primary_color': UnfoldAdminColorInputWidget(),
            'secondary_color': UnfoldAdminColorInputWidget(),
            'currency': UnfoldAdminTextInputWidget(),
            'currency_symbol': UnfoldAdminTextInputWidget(),
            
            'smtp_host': UnfoldAdminTextInputWidget(),
            'smtp_username': UnfoldAdminTextInputWidget(),
            'smtp_password': UnfoldAdminPasswordInputWidget(),
            
            'stripe_public_key': UnfoldAdminTextInputWidget(),
            'stripe_secret_key': UnfoldAdminPasswordInputWidget(),
            'stripe_webhook_secret': UnfoldAdminPasswordInputWidget(),
            
            'twilio_account_sid': UnfoldAdminTextInputWidget(),
            'twilio_auth_token': UnfoldAdminPasswordInputWidget(),
            'twilio_sender_number': UnfoldAdminTextInputWidget(),
        }

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(ModelAdmin):
    form = GlobalSettingsForm
    
    fieldsets = (
        ('✨ Brand Identity', {
            'fields': (('site_name', 'support_email'), ('site_logo', 'site_favicon'), ('primary_color', 'secondary_color'), ('currency', 'currency_symbol')),
            'classes': ('tab',),
            'description': 'Configure the core identity and appearance of the Aura platform globally.'
        }),
        ('💳 Payment Gateway', {
            'fields': ('stripe_public_key', 'stripe_secret_key', 'stripe_webhook_secret'),
            'classes': ('tab',),
            'description': 'Securely connect your Stripe account to process brand subscriptions and payouts.'
        }),
        ('📧 SMTP Mail Server', {
            'fields': (('smtp_host', 'smtp_port'), ('smtp_username', 'smtp_password')),
            'classes': ('tab',),
            'description': 'Setup external SMTP delivery for transactional emails and reports.'
        }),
        ('💬 SMS Gateway (Twilio)', {
            'fields': ('twilio_account_sid', 'twilio_auth_token', 'twilio_sender_number'),
            'classes': ('tab',),
            'description': 'Configure Twilio to send automated text messages and verification codes.'
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse
        obj, created = self.model.objects.get_or_create()
        return redirect(reverse('admin:%s_%s_change' % (self.opts.app_label, self.opts.model_name), args=[obj.id]))
"""

# Replace the existing GlobalSettingsAdmin
content = re.sub(r'@admin\.register\(GlobalSettings\).*?def changelist_view.*?\n        return redirect.*?args=\[obj\.id\]\)\)\n', new_admin_code, content, flags=re.DOTALL)

with open('apps/core/admin.py', 'w') as f:
    f.write(content)
print("Updated GlobalSettings")
