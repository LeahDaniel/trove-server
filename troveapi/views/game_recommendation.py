"""View module for handling requests about game recommendations"""
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from troveapi.models import GameRecommendation
from troveapi.views.user import UserSerializer


class GameRecommendationView(ViewSet):
    """Trove game_recommendation view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game_recommendation

        Returns:
            Response -- JSON serialized game_recommendation
        """
        try:
            game_recommendation = GameRecommendation.objects.get(pk=pk)
            serializer = RecoSerializer(game_recommendation)
            return Response(serializer.data)
        except GameRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game_recommendations

        Returns:
            Response -- JSON serialized list of game_recommendations
        """
        game_recommendations = GameRecommendation.objects.filter(
            recipient=request.auth.user)

        serializer = RecoSerializer(game_recommendations, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game_recommendation instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateRecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handle DELETE requests for a gameRecommendation

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            game_recommendation = GameRecommendation.objects.get(pk=pk)
            game_recommendation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except GameRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['put'], detail=False)
    def read(self, request):
        """Put requests to mark all of users received recommendations as read"""

        GameRecommendation.objects.filter(
            recipient=request.auth.user.id).update(read=True)

        return Response({'message': 'Game Recommendations marked as read'}, status=status.HTTP_204_NO_CONTENT)



class RecoSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    sender = UserSerializer(many=False)
    recipient = UserSerializer(many=False)

    class Meta:
        model = GameRecommendation
        depth = 1
        fields = ('id', 'game', 'recipient', 'message', 'sender')


class CreateRecoSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameRecommendation
        fields = ('id', 'game', 'recipient', 'message')