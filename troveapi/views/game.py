"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from troveapi.models import Game


class GameView(ViewSet):
    """Trove game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.filter(user=request.auth.user)

        search_text = request.query_params.get('search', None)
        # current must be passed in as string, not boolean 
        # due to diff between True and true in Python
        current_boolean = request.query_params.get('current', None)
        # multiplayer must be passed in as string, not boolean 
        multiplayer_boolean = request.query_params.get('multiplayer', None)
        # can be passed as int or string
        platform_id = request.query_params.get('platformId', None)
        tag_list = request.query_params.getlist('tags', '')

        filter_params = Q(user=request.auth.user)
        if search_text:
            filter_params &= Q(name__contains=search_text)
        if current_boolean:
            filter_params &= Q(current=current_boolean)
        if multiplayer_boolean:
            filter_params &= Q(multiplayer_capable=multiplayer_boolean)
        if platform_id:
            filter_params &= Q(platforms__id=platform_id)

        games = Game.objects.filter(filter_params)

        if tag_list:
            for tag_id in tag_list:
                games = games.filter(tags__id=tag_id)

        serializer = GameSerializer(games, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.save(user=user)

        game.tags.set(request.data["tags"])
        game.platforms.set(request.data["platforms"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            game = Game.objects.get(pk=pk)

            serializer = CreateGameSerializer(game, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_game = serializer.save()

            updated_game.tags.set(request.data["tags"])
            updated_game.platforms.set(request.data["platforms"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        depth = 1
        fields = ('id', 'multiplayer_capable', 'user',
                  'name', 'current', 'platforms', 'tags')


class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'multiplayer_capable', 'name',
                  'current', 'platforms', 'tags')
