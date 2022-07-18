from celery import shared_task

@shared_task(bind=True)
def send_notification(self):
    print("Here inside the send_notification function ")