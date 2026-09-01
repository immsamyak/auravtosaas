from django import template
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist

register = template.Library()

@register.simple_tag
def get_safe_template_path(template_path, fallback_path="storefront/default_section.html"):
    """
    Checks if a template exists. 
    If it does, returns the original path.
    If it doesn't, checks for a global fallback (e.g. storefront/global_newsletter.html).
    If that fails, returns the default fallback path.
    This prevents TemplateDoesNotExist 500 errors dynamically.
    """
    try:
        get_template(template_path)
        return template_path
    except TemplateDoesNotExist:
        try:
            # Extract section filename (e.g., newsletter.html)
            if '/sections/' in template_path:
                section_file = template_path.split('/sections/')[-1]
                global_path = f"storefront/global_{section_file}"
                get_template(global_path)
                return global_path
        except TemplateDoesNotExist:
            pass
        return fallback_path

@register.simple_tag
def filter_selected_items(queryset, selected_ids):
    """
    Filters a queryset by a list of selected IDs (used for explicit feature selections).
    If no selected_ids exist, returns the original queryset.
    """
    if selected_ids and isinstance(selected_ids, list) and len(selected_ids) > 0:
        # Convert IDs to integers safely
        ids = [int(i) for i in selected_ids if str(i).isdigit()]
        if ids:
            # Note: order_by doesn't preserve the exact order of the list in SQLite without a complex Case/When,
            # but filtering is sufficient for MVP.
            return queryset.filter(id__in=ids)
    return queryset
