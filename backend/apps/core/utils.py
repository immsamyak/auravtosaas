def notify(user, title, message, icon_class="fa-solid fa-bell", action_url=None):
    """
    Helper function to create notifications.
    """
    from apps.core.models import Notification
    
    if not user:
        return None
        
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        icon_class=icon_class,
        action_url=action_url
    )
