"""View module for handling requests about tag"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from troveapi.models import Tag


class TagView(ViewSet):
    """Trove tag view"""

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.order_by("tag").filter(user=request.auth.user)
        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tag types
    """
    class Meta:
        model = Tag
        fields = '__all__'