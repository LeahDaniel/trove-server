"""View module for handling requests about tag"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from troveapi.models import Tag
from rest_framework import serializers, status
from django.db.models import Count, Q
from django.contrib.auth.models import User


class TagView(ViewSet):
    """Trove tag view"""

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.order_by("tag").filter(user=request.auth.user)

        search_text = self.request.query_params.get('q', None)

        if search_text:
            tags = Tag.objects.order_by("tag").filter(
                Q(tag__contains=search_text) &
                Q(user=request.auth.user)
            )

        serializer = TagSerializer(tags, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized tag instance
        """
        user = User.objects.get(pk=request.auth.user.id)

        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            tag = Tag.objects.get(pk=pk)

            serializer = TagSerializer(tag, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tag types
    """
    class Meta:
        model = Tag
        fields = ('id', 'tag')
        
