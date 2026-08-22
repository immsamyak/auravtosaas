from typing import Any
from apps.core.models import SystemSetting, FeatureFlag, BrandSetting

class SettingsService:
    """
    Centralized service to fetch application-wide settings safely.
    """
    @staticmethod
    def get_setting(key: str, default: Any = None) -> Any:
        try:
            return SystemSetting.objects.get(key=key).value
        except SystemSetting.DoesNotExist:
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        value = SettingsService.get_setting(key)
        if value is None:
            return default
        return str(value).lower() in ('true', '1', 't', 'y', 'yes')

    @staticmethod
    def is_feature_enabled(feature_name: str) -> bool:
        try:
            return FeatureFlag.objects.get(name=feature_name).is_active
        except FeatureFlag.DoesNotExist:
            return False

class BrandSettingsService:
    """
    Service to fetch tenant-specific overrides, falling back to system defaults.
    """
    @staticmethod
    def get_currency(brand) -> str:
        try:
            return brand.settings.currency
        except (BrandSetting.DoesNotExist, AttributeError):
            return SettingsService.get_setting('DEFAULT_CURRENCY', 'USD')

    @staticmethod
    def get_tax_rate(brand) -> float:
        try:
            return float(brand.settings.tax_rate)
        except (BrandSetting.DoesNotExist, AttributeError):
            return float(SettingsService.get_setting('DEFAULT_TAX_RATE', '0.00'))
