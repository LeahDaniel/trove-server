"""View module for handling requests about streamingService"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from troveapi.models import StreamingService


class StreamingServiceView(ViewSet):
    """Trove streamingService view"""

    def list(self, request):
        """Handle GET requests to get all streamingServices

        Returns:
            Response -- JSON serialized list of streamingServices
        """
        streaming_services = StreamingService.objects.all()
        serializer = StreamingServiceSerializer(streaming_services, many=True)

        return Response(serializer.data)


class StreamingServiceSerializer(serializers.ModelSerializer):
    """JSON serializer for streamingService types
    """
    class Meta:
        model = StreamingService
        fields = '__all__'