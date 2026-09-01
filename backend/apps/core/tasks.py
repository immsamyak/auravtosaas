from celery import shared_task
from django.utils import timezone
from apps.core.email_utils import send_transactional_email
from apps.core.models import EmailLog
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_email_async(self, event_type, context, recipient_list):
    """
    Celery task to send an email asynchronously.
    """
    for recipient in recipient_list:
        # Create a pending EmailLog
        email_log = EmailLog.objects.create(
            recipient=recipient,
            subject=f"Processing {event_type}...", # Will be updated by send_transactional_email if successful
            template_type=event_type,
            status=EmailLog.Status.PENDING
        )
        try:
            success = send_transactional_email(event_type, context, [recipient])
            
            if success:
                email_log.status = EmailLog.Status.SENT
                email_log.sent_at = timezone.now()
                if isinstance(success, str):
                    email_log.subject = success
                else:
                    email_log.subject = f"Sent {event_type} to {recipient}"
                email_log.save()
            else:
                email_log.status = EmailLog.Status.FAILED
                email_log.error_message = "Email backend failed to send."
                email_log.save()
        except Exception as exc:
            logger.error(f"Error sending email {event_type} to {recipient}: {exc}")
            email_log.status = EmailLog.Status.FAILED
            email_log.error_message = str(exc)
            email_log.save()
            self.retry(exc=exc, countdown=60)
