from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from borrowing.tests.test_borrowing_signals_tasks_serializers import (
    sample_user,
    sample_book,
    sample_borrowing,
)
from payments.models import Payment
from payments.utils import create_stripe_session


class StripeSessionTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.book = sample_book(daily_fee=2)
        self.borrowing = sample_borrowing(user=self.user, book=self.book)
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = self.user

    @patch("payments.utils.stripe.checkout.Session.create")
    def test_create_stripe_session_creates_payment_and_returns_session(
        self, mock_create
    ):
        mock_session = MagicMock()
        mock_session.url = "http://stripe.test/session"
        mock_session.id = "sess_test_123"
        mock_create.return_value = mock_session

        session = create_stripe_session(self.borrowing, self.request)

        mock_create.assert_called_once()
        self.assertEqual(session.url, "http://stripe.test/session")

        payment = Payment.objects.get(borrowing_id=self.borrowing)
        self.assertEqual(payment.session_id, "sess_test_123")
        self.assertEqual(payment.status, Payment.Status.PENDING)
