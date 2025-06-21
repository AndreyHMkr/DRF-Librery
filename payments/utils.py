import stripe
from django.conf import settings

from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing):
    days = (borrowing.expected_return_date - borrowing.borrowing_date).days
    amount = borrowing.book.daily_fee * days

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Library payment"},
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )

    Payment.objects.create(
        status=Payment.Status.PENDING,
        type=Payment.Type.PAYMENT,
        borrowing_id=borrowing,
        session_url=session.url,
        session_id=session.id,
    )
    return session
