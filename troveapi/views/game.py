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

        search_text = self.request.query_params.get('q', None)
        current_text = self.request.query_params.get('current', None)

        if search_text and current_text:
            games = Game.objects.filter(
                Q(name__contains=search_text) &
                Q(current=current_text) &
                Q(user=request.auth.user)
            )
        elif search_text:
            games = Game.objects.filter(
                Q(name__contains=search_text) &
                Q(user=request.auth.user)
            )
        elif current_text:
            games = Game.objects.filter(
                Q(current=current_text) &
                Q(user=request.auth.user)
            )

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
