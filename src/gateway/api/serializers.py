from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    data = serializers.JSONField()

    class Meta:
        swagger_schema_fields = {
            "example": {
                "data": {"test": "hi"},
            },
        }
