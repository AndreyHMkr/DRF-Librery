from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from books_service.models import Book
from books_service.serializers import BookSerializer
from user.permissions import IsAdminOllActionOllReadOnlyAndBorrowingAction


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOllActionOllReadOnlyAndBorrowingAction]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "books",
                type={"type": "array", "items": {"type": "string"}},
                description="List all books for oll users",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "books",
                type={"type": "array", "items": {"type": "string"}},
                description="Only admin can crate new books",
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "books/<int:id>",
                type={"type": "array", "items": {"type": "integer"}},
                description="Get book by id",
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
