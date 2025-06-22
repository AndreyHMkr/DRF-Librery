from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books_service.models import Book
from borrowing.models import Borrowing
from user.models import User

BORROWING_URL = reverse("borrowing-list")


def sample_user(**params):
    defaults = {"email": "test@example.com", "password": "pass1234"}
    defaults.update(params)
    return User.objects.create_user(**defaults)


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "SOFT",
        "inventory": 5,
        "daily_fee": 2.5,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


def sample_borrowing(user, **param) -> Borrowing:
    default = {
        "borrowing_date": "2025-06-22",
        "expected_return_date": timezone.localdate(),
        "book": sample_book(),
        "user": user,
    }
    default.update(param)
    return Borrowing.objects.create(**default)


class BorrowingListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.other_user = sample_user(email="test1@example.com")
        self.book = sample_book()
        self.client.force_authenticate(user=self.user)

        sample_borrowing(user=self.user, book=self.book)

        sample_borrowing(user=self.other_user, book=self.book)

    def test_user_sees_only_their_borrowings(self):
        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        borrowing = response.data[0]
        self.assertEqual(borrowing["book"], "Test Book")

    def test_list_with_is_active_true(self):
        active_borrowing = sample_borrowing(user=self.user, book=self.book)
        returned_borrowing = sample_borrowing(
            user=self.user, book=self.book, actual_return_date=timezone.localdate()
        )

        response = self.client.get(BORROWING_URL + "?is_active=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {item["id"] for item in response.data}
        self.assertIn(active_borrowing.id, ids)
        self.assertNotIn(returned_borrowing.id, ids)

    def test_list_with_is_active_false(self):
        sample_borrowing(user=self.user, book=self.book)
        returned_borrowing = sample_borrowing(
            user=self.user, book=self.book, actual_return_date=timezone.localdate()
        )

        response = self.client.get(BORROWING_URL + "?is_active=false")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], returned_borrowing.id)

    def test_admin_sees_all_borrowings(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
