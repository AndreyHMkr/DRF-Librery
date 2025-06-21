from rest_framework import serializers

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrowing_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "user")


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    is_returned = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrowing_date",
            "expected_return_date",
            "book",
            "user",
            "is_returned",
        )

    def get_is_returned(self, obj):
        return obj.actual_return_date is not None


class BorrowingRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrowing_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
