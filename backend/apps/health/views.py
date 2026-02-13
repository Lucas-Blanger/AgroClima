from django.db import connections
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_status = "ok"

        try:
            connections["default"].cursor()
        except Exception:
            db_status = "error"

        return Response(
            {
                "status": "ok",
                "database": db_status,
                "timestamp": now(),
            }
        )
