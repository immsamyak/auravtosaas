filepath = 'apps/core/email_utils.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """def dispatch_async_email(event_type, context, to_emails, brand=None):
    \"\"\"
    Fire-and-forget email dispatcher using Celery.
    \"\"\"
    if brand:
        context['brand_name'] = brand.name
        if brand.logo:
            context['brand_logo'] = brand.logo.url
    
    from apps.core.tasks import send_email_async
    send_email_async.delay(event_type, context, to_emails)"""

replacement = """def dispatch_async_email(event_type, context, to_emails, brand=None):
    \"\"\"
    Fire-and-forget email dispatcher using Celery (or sync fallback).
    \"\"\"
    if brand:
        context['brand_name'] = brand.name
        if brand.logo:
            context['brand_logo'] = brand.logo.url
    
    try:
        from apps.core.tasks import send_email_async
        send_email_async.delay(event_type, context, to_emails)
    except (ImportError, Exception):
        # Fallback to synchronous if celery is not configured or fails
        try:
            from apps.core.tasks import send_email_async
            send_email_async(event_type, context, to_emails)
        except Exception as e:
            print(f"Failed to send email synchronously: {e}")"""

if target in content:
    content = content.replace(target, replacement)

with open(filepath, 'w') as f:
    f.write(content)
