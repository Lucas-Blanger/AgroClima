from django.db import models


class WeatherAlert(models.Model):
    city = models.CharField(max_length=100)
    aler_t_type = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
