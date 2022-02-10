"""View module for handling requests about show recommendations"""
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from troveapi.models import ShowRecommendation


class ShowRecommendationView(ViewSet):
    """Trove show_recommendation view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single show_recommendation

        Returns:
            Response -- JSON serialized show_recommendation
        """
        try:
            show_recommendation = ShowRecommendation.objects.get(pk=pk)
            serializer = RecoSerializer(show_recommendation)
            return Response(serializer.data)
        except ShowRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all show_recommendations

        Returns:
            Response -- JSON serialized list of show_recommendations
        """
        show_recommendations = ShowRecommendation.objects.filter(
            recipient=request.auth.user)

        serializer = RecoSerializer(show_recommendations, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized show_recommendation instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateRecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handle DELETE requests for a showRecommendation

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            show_recommendation = ShowRecommendation.objects.get(pk=pk)
            show_recommendation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ShowRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=False)
    def read(self, request):
        """Put requests to mark all of users received recommendations as read"""

        ShowRecommendation.objects.filter(
            recipient=request.auth.user.id).update(read=True)

        return Response({'message': 'Show Recommendations marked as read'}, status=status.HTTP_204_NO_CONTENT)


class RecoSerializer(serializers.ModelSerializer):
    """JSON serializer for show types
    """
    class Meta:
        model = ShowRecommendation
        depth = 2
        fields = '__all__'


class CreateRecoSerializer(serializers.ModelSerializer):
    """JSON serializer for show types
    """
    class Meta:
        model = ShowRecommendation
        fields = ('id', 'show', 'recipient', 'message')
