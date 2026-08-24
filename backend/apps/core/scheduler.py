from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def process_scheduled_campaigns():
    from .models import NotificationCampaign
    from .notifications import NotificationManager
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Find scheduled campaigns
    campaigns = NotificationCampaign.objects.filter(
        status=NotificationCampaign.Status.SCHEDULED,
        scheduled_for__lte=timezone.now()
    )
    
    for campaign in campaigns:
        campaign.status = NotificationCampaign.Status.SENDING
        campaign.save(update_fields=['status'])
        
        try:
            # Determine recipients
            if campaign.target_audience == NotificationCampaign.TargetAudience.ALL_USERS:
                recipients = User.objects.filter(is_active=True)
            elif campaign.target_audience == NotificationCampaign.TargetAudience.ALL_BRANDS:
                # Assuming brands are users with a brand profile
                recipients = User.objects.filter(is_active=True, brands__isnull=False).distinct()
            elif campaign.target_audience == NotificationCampaign.TargetAudience.ALL_CONSUMERS:
                recipients = User.objects.filter(is_active=True, profile__isnull=False).distinct()
            else:
                recipients = campaign.specific_users.filter(is_active=True)
                
            for recipient in recipients:
                if recipient.email:
                    NotificationManager.send_custom_campaign(recipient, campaign)
                    
            campaign.status = NotificationCampaign.Status.SENT
            campaign.sent_at = timezone.now()
            campaign.save(update_fields=['status', 'sent_at'])
            logger.info(f"Successfully sent campaign: {campaign.subject}")
            
        except Exception as e:
            campaign.status = NotificationCampaign.Status.FAILED
            campaign.save(update_fields=['status'])
            logger.error(f"Failed to send campaign {campaign.id}: {e}")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_scheduled_campaigns, 'interval', minutes=1, id='campaign_job', replace_existing=True)
    scheduler.start()
    logger.info("Notification scheduler started.")
