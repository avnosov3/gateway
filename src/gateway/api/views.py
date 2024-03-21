import json

from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.settings import DJANGO_CACHE_TIME
from gateway.api.serializers import RequestSerializer
from gateway.http_client import CELERY_ID
from gateway.tasks import send_request_to_receiver


class GatewayCreateView(APIView):

    @swagger_auto_schema(
        request_body=RequestSerializer,
        responses={
            200: openapi.Response(
                description="Request was accepted",
                examples={"application/json": {"message": "Request accepted", "data": {"key": "value"}}},
            ),
        },
        tags=["gateway"],
    )
    def post(self, request):
        try:
            serializer = RequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data["data"]
            cache_key = hash(json.dumps(data))
            if cache.get(cache_key):
                celery_id = cache.get(cache_key)
            else:
                task = send_request_to_receiver.delay(data)
                celery_id = task.id
                cache.set(cache_key, celery_id, timeout=DJANGO_CACHE_TIME)
            headers = {CELERY_ID: celery_id}
            return Response({"message": "Request accepted"}, status=status.HTTP_200_OK, headers=headers)
        except ValidationError as error:
            return Response({"message": f"Validation error: {str(error)}"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message": f"Unexpected error: {str(error)}"}, status=status.HTTP_200_OK)
