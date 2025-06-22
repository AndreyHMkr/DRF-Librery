from django.utils.timezone import now
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
)
from user.permissions import IsAdminOrReadOnlyBorrowing


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyBorrowing]

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "This book is out of stock. Please try again later."
            )
        book.inventory -= 1
        book.save()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )

        borrowing.actual_return_date = now().date()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()
        return Response({"status": "book returned"})

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)
        return queryset.select_related("user", "book")
