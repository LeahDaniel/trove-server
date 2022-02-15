"""View module for handling requests about books"""
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from troveapi.models import Book
from troveapi.views.user import UserSerializer


class BookView(ViewSet):
    """Trove book view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book

        Returns:
            Response -- JSON serialized book
        """
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all books

        Returns:
            Response -- JSON serialized list of books
        """
        search_text = request.query_params.get('search', None)
        # current must be passed in as string, not boolean
        # due to diff between True and true in Python
        current_boolean = request.query_params.get('current', None)
        # can be passed as int or string
        author_id = request.query_params.get('authorId', None)
        tag_list = request.query_params.getlist('tags', '')

        filter_params = Q(user=request.auth.user)
        if search_text:
            filter_params &= Q(name__icontains=search_text)
        if current_boolean:
            filter_params &= Q(current=current_boolean)
        if author_id:
            filter_params &= Q(author__id=author_id)

        books = Book.objects.filter(filter_params).order_by('-last_modified')

        if tag_list:
            for tag_id in tag_list:
                books = books.filter(tags__id=tag_id)

        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized book instance
        """

        user = User.objects.get(pk=request.auth.user.id)

        serializer = CreateBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save(user=user)

        book.tags.set(request.data["tags"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a book

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            book = Book.objects.get(pk=pk)

            serializer = CreateBookSerializer(book, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_book = serializer.save()

            updated_book.tags.set(request.data["tags"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a book

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Book
        depth = 1
        fields = ('id', 'user',
                  'name', 'current', 'author', 'tags')


class CreateBookSerializer(serializers.ModelSerializer):
    """JSON serializer for book types
    """
    class Meta:
        model = Book
        fields = ('id', 'name',
                  'current', 'author', 'tags')
