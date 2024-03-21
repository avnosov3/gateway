from core.api_gateaway_urls import API_GATEAWAY_URL
from core.base_http_client import BaseSyncClient

CELERY_ID = "X-Celery-ID"
RETRIES = "X-Retries"


class GatewayClient(BaseSyncClient):

    def pass_request(self, celery_id, data, retries, url=API_GATEAWAY_URL):
        headers = {CELERY_ID: celery_id, RETRIES: str(retries)}
        request_params = dict(url=url, headers=headers, data=data)
        return self.post(**request_params)


gateway_client = GatewayClient()
