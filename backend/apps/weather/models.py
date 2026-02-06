from django.db import models
from django.utils import timezone


class WeatherCurrent(models.Model):
    # Dados climáticos atuais

    temperature = models.FloatField(help_text="Temperatura em Celsius")
    feels_like = models.FloatField(help_text="Sensação térmica")
    temp_min = models.FloatField(help_text="Temperatura mínima")
    temp_max = models.FloatField(help_text="Temperatura máxima")
    humidity = models.IntegerField(help_text="Umidade em %")
    pressure = models.IntegerField(help_text="Pressão atmosférica em hPa")
    wind_speed = models.FloatField(help_text="Velocidade do vento em m/s")
    wind_deg = models.IntegerField(help_text="Direção do vento em graus")
    clouds = models.IntegerField(help_text="Nebulosidade em %")
    rain_1h = models.FloatField(
        null=True, blank=True, help_text="Chuva última hora em mm"
    )
    rain_3h = models.FloatField(
        null=True, blank=True, help_text="Chuva últimas 3h em mm"
    )
    description = models.CharField(max_length=200, help_text="Descrição do clima")
    icon = models.CharField(max_length=10, help_text="Código do ícone")
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Clima Atual"
        verbose_name_plural = "Clima Atual"

    def __str__(self):
        return f"Clima atual - {self.updated_at.strftime('%d/%m/%Y %H:%M')}"


class WeatherForecast(models.Model):
    # Previsão do tempo para os próximos dias

    date = models.DateField(help_text="Data da previsão")
    temp_min = models.FloatField(help_text="Temperatura mínima")
    temp_max = models.FloatField(help_text="Temperatura máxima")
    humidity = models.IntegerField(help_text="Umidade média em %")
    pressure = models.IntegerField(help_text="Pressão atmosférica em hPa")
    wind_speed = models.FloatField(help_text="Velocidade do vento em m/s")
    clouds = models.IntegerField(help_text="Nebulosidade em %")
    rain = models.FloatField(default=0, help_text="Precipitação esperada em mm")
    pop = models.FloatField(help_text="Probabilidade de precipitação (0-1)")
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date"]
        unique_together = ["date"]
        verbose_name = "Previsão do Tempo"
        verbose_name_plural = "Previsões do Tempo"

    def __str__(self):
        return f"Previsão {self.date.strftime('%d/%m/%Y')}"


class WeatherAlert(models.Model):
    # Alertas climáticos

    SEVERITY_CHOICES = [
        ("low", "Baixa"),
        ("medium", "Média"),
        ("high", "Alta"),
        ("extreme", "Extrema"),
    ]

    event = models.CharField(max_length=200, help_text="Tipo de evento")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-severity", "-start_time"]
        verbose_name = "Alerta Climático"
        verbose_name_plural = "Alertas Climáticos"

    def __str__(self):
        return f"{self.event} - {self.severity}"

    def save(self, *args, **kwargs):
        # Desativa alerta se data final passou
        if self.end_time < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)
