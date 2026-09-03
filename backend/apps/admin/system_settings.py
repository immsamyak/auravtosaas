from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.core.models import SystemSetting, FeatureFlag, BrandSetting

@admin.register(SystemSetting)
class SystemSettingAdmin(ModelAdmin):
    list_display = ('key', 'category', 'value', 'updated_at')
    list_filter = ('category',)
    search_fields = ('key', 'value')

from unfold.decorators import display
from django import forms
from unfold.widgets import UnfoldBooleanWidget, UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

class FeatureFlagAdminForm(forms.ModelForm):
    class Meta:
        model = FeatureFlag
        fields = '__all__'
        widgets = {
            'name': UnfoldAdminTextInputWidget(),
            'is_active': UnfoldBooleanWidget(),
        }

@admin.register(FeatureFlag)
class FeatureFlagAdmin(ModelAdmin):
    form = FeatureFlagAdminForm
    list_display = ('name', 'is_active_badge')
    list_filter = ('is_active',)
    search_fields = ('name',)
    
    @display(description="Status", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active
        
    fieldsets = (
        ('Feature Toggle', {
            'fields': ('name', 'is_active'),
            'classes': ('tab',)
        }),
    )

class BrandSettingAdminForm(forms.ModelForm):
    class Meta:
        model = BrandSetting
        fields = '__all__'
        widgets = {
            'brand': UnfoldAdminSelectWidget(),
            'currency': UnfoldAdminTextInputWidget(),
            'tax_rate': UnfoldAdminTextInputWidget(),
        }

@admin.register(BrandSetting)
class BrandSettingAdmin(ModelAdmin):
    form = BrandSettingAdminForm
    list_display = ('brand', 'currency', 'tax_rate')
    search_fields = ('brand__name', 'currency')
    
    fieldsets = (
        ('Brand Defaults', {
            'fields': ('brand', 'currency', 'tax_rate'),
            'classes': ('tab',)
        }),
    )

from unfold.admin import TabularInline
from apps.core.models import LandingPageConfig, LandingPageFeature

class LandingPageFeatureInline(TabularInline):
    model = LandingPageFeature
    extra = 1

from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminTextareaWidget
from django import forms

class LandingPageConfigForm(forms.ModelForm):
    class Meta:
        model = LandingPageConfig
        fields = '__all__'
        widgets = {
            'hero_headline': UnfoldAdminTextInputWidget(attrs={'class': 'font-bold text-xl'}),
            'hero_subheadline': UnfoldAdminTextareaWidget(),
            'hero_primary_cta': UnfoldAdminTextInputWidget(),
            'hero_secondary_cta': UnfoldAdminTextInputWidget(),
            'demo_title': UnfoldAdminTextInputWidget(),
            'demo_subtitle': UnfoldAdminTextInputWidget(),
            'footer_text': UnfoldAdminTextInputWidget(),
            'is_active': UnfoldBooleanWidget(),
        }

@admin.register(LandingPageConfig)
class LandingPageConfigAdmin(ModelAdmin):
    form = LandingPageConfigForm
    list_display = ('__str__', 'is_active_badge', 'updated_at')
    list_filter = ('is_active',)
    inlines = [LandingPageFeatureInline]
    
    @display(description="Status", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active
    
    fieldsets = (
        ('Hero Section', {
            'fields': (('hero_headline', 'hero_subheadline'), ('hero_primary_cta', 'hero_secondary_cta')),
            'classes': ('tab',),
        }),
        ('Demo Section', {
            'fields': ('demo_subtitle', 'demo_title'),
            'classes': ('tab',),
        }),
        ('Footer & Status', {
            'fields': ('footer_text', 'is_active'),
            'classes': ('tab',),
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

from apps.core.models import Page, FooterSection, FooterLink
from unfold.widgets import UnfoldAdminTextareaWidget

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'title': UnfoldAdminTextInputWidget(),
            'slug': UnfoldAdminTextInputWidget(),
            'content': UnfoldAdminTextareaWidget(),
            'is_published': UnfoldBooleanWidget(),
        }

@admin.register(Page)
class PageAdmin(ModelAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'is_published_badge', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    @display(description="Published", boolean=True)
    def is_published_badge(self, obj):
        return obj.is_published
        
    fieldsets = (
        ('Page Content', {
            'fields': (('title', 'slug'), 'content'),
            'classes': ('tab',)
        }),
        ('Visibility', {
            'fields': ('is_published',),
            'classes': ('tab',)
        }),
    )

class FooterLinkInline(TabularInline):
    model = FooterLink
    extra = 1

class FooterSectionAdminForm(forms.ModelForm):
    class Meta:
        model = FooterSection
        fields = '__all__'
        widgets = {
            'title': UnfoldAdminTextInputWidget(),
            'display_order': UnfoldAdminTextInputWidget(),
        }

@admin.register(FooterSection)
class FooterSectionAdmin(ModelAdmin):
    form = FooterSectionAdminForm
    list_display = ('title', 'display_order')
    inlines = [FooterLinkInline]
    ordering = ('display_order',)

from apps.core.models import GlobalSettings


from django import forms
from unfold.widgets import (
    UnfoldAdminTextInputWidget,
    UnfoldAdminColorInputWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminPasswordWidget
)

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = '__all__'
        widgets = {
            'site_name': UnfoldAdminTextInputWidget(attrs={'class': 'font-bold text-xl'}),
            'support_email': UnfoldAdminEmailInputWidget(),
            'email_sender_address': UnfoldAdminEmailInputWidget(),
            'site_logo': UnfoldAdminImageFieldWidget(),
            'site_favicon': UnfoldAdminImageFieldWidget(),
            'primary_color': UnfoldAdminColorInputWidget(),
            'secondary_color': UnfoldAdminColorInputWidget(),
            'currency': UnfoldAdminTextInputWidget(),
            'currency_symbol': UnfoldAdminTextInputWidget(),
            
            'vto_engine': forms.Select(attrs={'class': 'border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm px-3 py-2'}),
            'replicate_api_key': UnfoldAdminPasswordWidget(),
            'replicate_model_version': UnfoldAdminTextInputWidget(),
            
            
            'smtp_host': UnfoldAdminTextInputWidget(),
            'smtp_username': UnfoldAdminTextInputWidget(),
            'stripe_environment': forms.Select(attrs={'class': 'border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm px-3 py-2'}),
            'stripe_test_public_key': UnfoldAdminTextInputWidget(),
            'stripe_test_secret_key': UnfoldAdminPasswordWidget(),
            'stripe_test_webhook_secret': UnfoldAdminPasswordWidget(),
            'stripe_live_public_key': UnfoldAdminTextInputWidget(),
            'stripe_live_secret_key': UnfoldAdminPasswordWidget(),
            'stripe_live_webhook_secret': UnfoldAdminPasswordWidget(),
            
            'twilio_account_sid': UnfoldAdminTextInputWidget(),
            'twilio_auth_token': UnfoldAdminPasswordWidget(),
            'twilio_sender_number': UnfoldAdminTextInputWidget(),
        }

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(ModelAdmin):
    form = GlobalSettingsForm
    
    fieldsets = (
        ('Brand Identity', {
            'fields': (('site_name', 'support_email'), ('site_logo', 'site_favicon'), ('primary_color', 'secondary_color'), ('currency', 'currency_symbol')),
            'classes': ('tab',),
            'description': 'Configure the core identity and appearance of the Aura platform globally.'
        }),
        ('Virtual Try-On (VTO) AI Engine', {
            'fields': ('vto_engine', 'replicate_api_key', 'replicate_model_version', 'hf_space_id', 'hf_api_token'),
            'classes': ('tab',),
            'description': 'Configure which AI Model engine powers the Virtual Try-On feature across all brands. Using Replicate is highly recommended for production servers to prevent memory crashes.'
        }),
        ('Payment Gateway', {
            'fields': ('stripe_environment', ('stripe_test_public_key', 'stripe_live_public_key'), ('stripe_test_secret_key', 'stripe_live_secret_key'), ('stripe_test_webhook_secret', 'stripe_live_webhook_secret')),
            'classes': ('tab',),
            'description': 'Securely connect your Stripe account to process brand subscriptions and payouts.'
        }),
        ('SMTP Mail Server', {
            'fields': (('smtp_host', 'smtp_port'), ('smtp_username', 'smtp_password')),
            'classes': ('tab',),
            'description': 'Setup external SMTP delivery for transactional emails and reports.'
        }),
        ('SMS Gateway (Twilio)', {
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

from apps.core.models import Testimonial
from unfold.widgets import UnfoldAdminTextareaWidget

class TestimonialAdminForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = {
            'author_name': UnfoldAdminTextInputWidget(),
            'author_title': UnfoldAdminTextInputWidget(),
            'quote': UnfoldAdminTextareaWidget(),
            'is_active': UnfoldBooleanWidget(),
        }

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    form = TestimonialAdminForm
    list_display = ('author_name', 'author_title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author_name', 'quote')

from apps.core.models import PlatformIntegration

class PlatformIntegrationAdminForm(forms.ModelForm):
    class Meta:
        model = PlatformIntegration
        fields = '__all__'
        widgets = {
            'name': UnfoldAdminTextInputWidget(),
            'provider_code': UnfoldAdminTextInputWidget(),
            'category': UnfoldAdminSelectWidget(),
            'is_active_globally': UnfoldBooleanWidget(),
        }

@admin.register(PlatformIntegration)
class PlatformIntegrationAdmin(ModelAdmin):
    form = PlatformIntegrationAdminForm
    list_display = ('name', 'provider_code', 'category', 'is_active_globally')
    list_filter = ('category', 'is_active_globally')
    search_fields = ('name', 'provider_code')

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
