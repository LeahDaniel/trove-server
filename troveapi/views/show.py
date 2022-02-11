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

        search_text = request.query_params.get('search', None)
        # current must be passed in as string, not boolean 
        # due to diff btwn True and true in Python
        current_boolean = request.query_params.get('current', None)
        # can be passed as int or string
        streaming_service_id = request.query_params.get('streamingServiceId', None)
        tag_list = request.query_params.getlist('tags', '')

        filter_params = Q(user=request.auth.user)
        if search_text:
            filter_params &= Q(name__contains=search_text)
        if current_boolean:
            filter_params &= Q(current=current_boolean)
        if streaming_service_id:
            filter_params &= Q(streaming_service__id=streaming_service_id)

        shows = Show.objects.filter(filter_params)

        if tag_list:
            for tag_id in tag_list:
                shows = shows.filter(tags__id=tag_id)

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
