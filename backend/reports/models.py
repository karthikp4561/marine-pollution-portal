from django.db import models


class PollutionReport(models.Model):
    pollution_type = models.CharField(max_length=100)
    description = models.TextField()

    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='pollution_reports/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pollution_type