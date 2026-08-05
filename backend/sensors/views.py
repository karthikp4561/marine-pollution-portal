from rest_framework import viewsets
from .models import SensorData
from .serializers import SensorDataSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all().order_by("-created_at")
    serializer_class = SensorDataSerializer