from celery import shared_task


@shared_task(bind=True)
def send_slack_notification(self):
    """
    slack webhook integration here
    Ellipses as placeholder for now
    """
    ...
