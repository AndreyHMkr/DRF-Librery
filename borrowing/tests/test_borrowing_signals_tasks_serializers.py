from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import localdate
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from books_service.models import Book
from borrowing.models import Borrowing
from borrowing.tasks import check_overdue_borrowings
from user.models import User

BORROWING_URL = reverse("borrowing-list")


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


def sample_user(**params):
    defaults = {"email": "test@example.com", "password": "pass1234"}
    defaults.update(params)
    return User.objects.create_user(**defaults)


def sample_borrowing(user, **param) -> Borrowing:
    default = {
        "borrowing_date": localdate(),
        "expected_return_date": timezone.localdate(),
        "book": sample_book(),
        "user": user,
    }
    default.update(param)
    return Borrowing.objects.create(**default)


class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD111>",
        )
        self.client.force_authenticate(user=self.user)

    def test_auth_user_can_create_borrow(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_borrowing(self):
        sample_borrowing(user=self.user)
        response = self.client.get(BORROWING_URL)
        borrowing_data = response.data[0]
        self.assertEqual(borrowing_data["book"], "Test Book")
        self.assertEqual(borrowing_data["borrowing_date"], str(timezone.localdate()))
        self.assertEqual(
            borrowing_data["expected_return_date"], str(timezone.localdate())
        )


class BorrowingSingleTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.book = sample_book()

    @patch("borrowing.signals.send_telegram_message")
    def test_send_telegram_message(self, mock_signal):
        borrowing = sample_borrowing(self.user)
        expected_message = (
            f"📚 <b>New Borrowing Created</b>\n"
            f"User: {self.user.email}\n"
            f"Book: <i>{self.book.title}</i>\n"
            f"Borrow date: {borrowing.borrowing_date}\n"
            f"Expected return: {borrowing.expected_return_date}"
        )
        mock_signal.assert_called_once_with(expected_message)

    @patch("borrowing.signals.send_telegram_message")
    def test_send_telegram_message_with_borrowing(self, mock_signal):
        borrowing = sample_borrowing(self.user)
        borrowing.actual_return_date = timezone.localdate()
        borrowing.save()

        expected_message = (
            f"✅ <b>Book is returned</b>\n"
            f"User: {self.user.email}\n"
            f"Book: <i>{self.book.title}</i>\n"
            f"Data of returned: {borrowing.actual_return_date}"
        )

        mock_signal.assert_called_with(expected_message)


class CheckOverdueBorrowingTaskTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.book = sample_book()

    @patch("borrowing.tasks.send_telegram_message")
    def test_check_overdue_borrowing(self, mock_signal):
        overdue_date = timezone.localdate() - timezone.timedelta(days=3)
        borrowing_date = overdue_date - timezone.timedelta(days=2)

        sample_borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=overdue_date,
            borrowing_date=borrowing_date,
        )

        check_overdue_borrowings()

        mock_signal.assert_called_once()
        message = mock_signal.call_args[0][0]
        self.assertIn("❗ Overdue Borrowing Alert", message)
        self.assertIn(self.user.email, message)
        self.assertIn(self.book.title, message)

    @patch("borrowing.tasks.send_telegram_message")
    def test_check_overdue_borrowing_sends_no_overdue_message(self, mock_send):
        # All borrowings are returned
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrowing_date=timezone.localdate() - timezone.timedelta(days=5),
            expected_return_date=timezone.localdate() - timezone.timedelta(days=2),
            actual_return_date=timezone.localdate() - timezone.timedelta(days=1),
        )

        check_overdue_borrowings()

        mock_send.assert_called_once_with("✅ No borrowings overdue today!")
