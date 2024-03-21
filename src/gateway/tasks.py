import logging

from celery import shared_task

from core.settings import CELERY_RETRY_ATTEMPTS, CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS
from gateway.http_client import gateway_client

logger = logging.getLogger(__name__)

EIGTH_PER_SECOND = "8/s"


@shared_task(bind=True, rate_limit=EIGTH_PER_SECOND, default_retry_delay=CELERY_RETRY_ATTEMPTS)
def send_request_to_receiver(self, request_data):
    try:
        response = gateway_client.pass_request(
            celery_id=self.request.id, data=request_data, retries=self.request.retries
        )
    except Exception as error:
        logger.exception(error)
        raise self.retry(exc=error, countdown=CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS)
    return response.status_code
