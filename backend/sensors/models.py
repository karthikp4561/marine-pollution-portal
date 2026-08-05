from django.db import models


class SensorData(models.Model):
    buoy_id = models.CharField(max_length=100, default="BUOY_001")
    ph = models.FloatField()
    turbidity = models.FloatField()
    salinity = models.FloatField()
    oil_detected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buoy_id
