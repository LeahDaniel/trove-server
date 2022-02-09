"""View module for handling requests about shows"""
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from troveapi.models import Show


class ShowView(ViewSet):
    """Trove show view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single show

        Returns:
            Response -- JSON serialized show
        """
        try:
            show = Show.objects.get(pk=pk)
            serializer = ShowSerializer(show)
            return Response(serializer.data)
        except Show.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all shows

        Returns:
            Response -- JSON serialized list of shows
        """
        shows = Show.objects.filter(user=request.auth.user)

        search_text = self.request.query_params.get('q', None)
        current_text = self.request.query_params.get('current', None)

        if search_text and current_text:
            shows = Show.objects.filter(
                Q(name__contains=search_text) &
                Q(current=current_text) &
                Q(user=request.auth.user)
            )
        elif search_text:
            shows = Show.objects.filter(
                Q(name__contains=search_text) &
                Q(user=request.auth.user)
            )
        elif current_text:
            shows = Show.objects.filter(
                Q(current=current_text) &
                Q(user=request.auth.user)
            )

        serializer = ShowSerializer(shows, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized show instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateShowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        show = serializer.save(user=user)

        show.tags.set(request.data["tags"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a show

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            show = Show.objects.get(pk=pk)

            serializer = CreateShowSerializer(show, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_show = serializer.save()

            updated_show.tags.set(request.data["tags"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Show.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a show

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            show = Show.objects.get(pk=pk)
            show.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Show.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ShowSerializer(serializers.ModelSerializer):
    """JSON serializer for show types
    """
    class Meta:
        model = Show
        depth = 1
        fields = ('id', 'user',
                  'name', 'current', 'streaming_service', 'tags')


class CreateShowSerializer(serializers.ModelSerializer):
    """JSON serializer for show types
    """
    class Meta:
        model = Show
        fields = ('id', 'name',
                  'current', 'streaming_service', 'tags')
