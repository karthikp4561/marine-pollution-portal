from rest_framework import serializers
from .models import PollutionReport


class PollutionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollutionReport
        fields = '__all__'