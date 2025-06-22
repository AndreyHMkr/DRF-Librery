from rest_framework import serializers
from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowing.models import Borrowing
from payments.serializers import PaymentSerializer
from payments.utils import create_stripe_session
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrowing_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        validated_data["user"] = user
        borrowing = Borrowing.objects.create(**validated_data)
        create_stripe_session(borrowing, request)
        return borrowing

    def get_session_url(self, obj):
        latest_payment = obj.payments.order_by("-created_at").first()
        return latest_payment.session_url if latest_payment else None


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
