"""View module for handling requests about book recommendations"""
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from troveapi.models import BookRecommendation
from troveapi.views.user import UserSerializer


class BookRecommendationView(ViewSet):
    """Trove book_recommendation view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book_recommendation

        Returns:
            Response -- JSON serialized book_recommendation
        """
        try:
            book_recommendation = BookRecommendation.objects.get(pk=pk)
            serializer = RecoSerializer(book_recommendation)
            return Response(serializer.data)
        except BookRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all book_recommendations

        Returns:
            Response -- JSON serialized list of book_recommendations
        """
        book_recommendations = BookRecommendation.objects.filter(
            recipient=request.auth.user)

        serializer = RecoSerializer(book_recommendations, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized book_recommendation instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateRecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handle DELETE requests for a bookRecommendation

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            book_recommendation = BookRecommendation.objects.get(pk=pk)
            book_recommendation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except BookRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=False)
    def read(self, request):
        """Put requests to mark all of users received recommendations as read"""

        BookRecommendation.objects.filter(
            recipient=request.auth.user.id, read=False).update(read=True)

        return Response({'message': 'Book Recommendations marked as read'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def notify(self, request):
        """Put requests to mark all of users received recommendations as read"""

        unread = BookRecommendation.objects.filter(
            recipient=request.auth.user.id, read=False)

        if len(unread) > 0:
            return Response({'new': True})
        else:
            return Response({'new': False})


class RecoSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    sender = UserSerializer(many=False)
    recipient = UserSerializer(many=False)

    class Meta:
        model = BookRecommendation
        depth = 1
        fields = ('id', 'book', 'recipient', 'message', 'sender')


class CreateRecoSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    class Meta:
        model = BookRecommendation
        fields = ('id', 'book', 'recipient', 'message')
