"""View module for handling requests about user"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User


class UserView(ViewSet):
    """Trove user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        try:
            user = User.objects.get(username=request.data['username'])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = User
        fields = 'id', 'username'
