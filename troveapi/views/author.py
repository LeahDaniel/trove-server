"""View module for handling requests about author"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from troveapi.models import Author


class AuthorView(ViewSet):
    """Trove author view"""

    def list(self, request):
        """Handle GET requests to get all authors

        Returns:
            Response -- JSON serialized list of authors
        """
        authors = Author.objects.filter(user=request.auth.user)
        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data)


class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for author types
    """
    class Meta:
        model = Author
        fields = '__all__'