import re

with open('backend/apps/orders/models.py', 'r') as f:
    content = f.read()

# I will just revert to the original, and then fix it properly.
def repl(m):
    return """    if not instance._state.adding:
        try:
            old_order = Order.objects.get(pk=instance.id)
            if old_order.status != 'PAID' and instance.status == 'PAID':
                try:
                    NotificationManager.send_order_confirmation(instance)
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f"Failed to send order confirmation: {e}")
        except Order.DoesNotExist:
            pass"""

# Since I messed up the block, I'll search for the current messed up block and replace it
content = re.sub(
    r'    if not instance\._state\.adding:\n        try:\n            old_order = Order\.objects\.get\(pk=instance\.id\)\n            if old_order\.status != \'PAID\' and instance\.status == \'PAID\':\n            try:\n                NotificationManager\.send_order_confirmation\(instance\)\n            except Exception as e:\n                import logging\n                logging\.getLogger\(__name__\)\.error\(f"Failed to send order confirmation: \{e\}"\)',
    repl,
    content
)

with open('backend/apps/orders/models.py', 'w') as f:
    f.write(content)

