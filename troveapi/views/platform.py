"""View module for handling requests about platform"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from troveapi.models import Platform


class PlatformView(ViewSet):
    """Trove platform view"""

    def list(self, request):
        """Handle GET requests to get all platforms

        Returns:
            Response -- JSON serialized list of platforms
        """
        platforms = Platform.objects.all()
        serializer = PlatformSerializer(platforms, many=True)

        return Response(serializer.data)


class PlatformSerializer(serializers.ModelSerializer):
    """JSON serializer for platform types
    """
    class Meta:
        model = Platform
        fields = '__all__'
