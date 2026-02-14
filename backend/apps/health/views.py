from django.db import connections
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.health.serializers import HealthSerializer


class HealthCheckView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = HealthSerializer

    def get(self, request, *args, **kwargs):
        db_status = "ok"

        try:
            connections["default"].cursor()
        except Exception:
            db_status = "error"

        data = {
            "status": "ok",
            "database": db_status,
            "timestamp": now(),
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)
