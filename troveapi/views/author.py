"""View module for handling requests about author"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from troveapi.models import Author
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework.decorators import action


class AuthorView(ViewSet):
    """Trove author view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single author

        Returns:
            Response -- JSON serialized author
        """
        try:
            name_text = self.request.query_params.get('name', None)
            author = Author.objects.get(name__iexact=name_text)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Author.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all authors

        Returns:
            Response -- JSON serialized list of authors
        """
        authors = Author.objects.filter(
            user=request.auth.user).order_by('name')

        name_text = self.request.query_params.get('name', None)

        if name_text:
            authors = Author.objects.filter(
                name__iexact=name_text, user=request.auth.user)

        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized author instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateAuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def active_current(self, request):
        """Only get actors back that are currently active on a book"""

        authors = Author.objects.annotate(
            count_book=Count('book_author')
        ).filter(count_book__gt=0, user=request.auth.user, book_author__current=True)

        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def active_queued(self, request):
        """Only get actors back that are currently active on a book"""

        authors = Author.objects.annotate(
            count_book=Count('book_author')
        ).filter(count_book__gt=0, user=request.auth.user, book_author__current=False)

        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data)


class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for author types
    """
    class Meta:
        model = Author
        fields = '__all__'


class CreateAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for author types
    """
    class Meta:
        model = Author
        fields = 'id', 'name'
