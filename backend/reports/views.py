from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PollutionReport
from .serializers import PollutionReportSerializer


class PollutionReportViewSet(viewsets.ModelViewSet):
    serializer_class = PollutionReportSerializer

    def get_queryset(self):
        return PollutionReport.objects.all().order_by('-created_at')

    @action(detail=False, methods=['get'])
    def approved(self, request):
        approved_reports = PollutionReport.objects.filter(
            status='approved'
        ).order_by('-created_at')

        serializer = self.get_serializer(approved_reports, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        report = self.get_object()
        report.status = 'approved'
        report.save()

        return Response({'message': 'Report approved'})

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        report = self.get_object()
        report.status = 'rejected'
        report.save()

        return Response({'message': 'Report rejected'})
    
    