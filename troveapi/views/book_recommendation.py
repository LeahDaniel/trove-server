"""View module for handling requests about book recommendations"""
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from troveapi.models import BookRecommendation


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

    def update(self, request, pk):
        """Handle PUT requests for a book_recommendation

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            book_recommendation = BookRecommendation.objects.get(pk=pk)

            book_recommendation.read = True
            book_recommendation.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except BookRecommendation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

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


class RecoSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    class Meta:
        model = BookRecommendation
        depth = 2
        fields = '__all__'


class CreateRecoSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    class Meta:
        model = BookRecommendation
        fields = ('id', 'book', 'recipient', 'message')
