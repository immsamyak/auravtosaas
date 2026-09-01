import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.core.email_utils import dispatch_async_email
from apps.core.utils import get_brand_url
from apps.catalog.models import ProductVariant

logger = logging.getLogger(__name__)

# Stock signals have been moved to StockLevel logic since ProductVariant does not track stock directly.
