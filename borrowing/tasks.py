from celery import shared_task
from django.utils.timezone import now
from telegram_notifications.utils.telegram import send_telegram_message
from borrowing.models import Borrowing


@shared_task
def check_overdue_borrowings():
    today = now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today, actual_return_date__isnull=True
    )

    if not overdue_borrowings.exists():
        send_telegram_message("✅ No borrowings overdue today!")
        return

    for borrowing in overdue_borrowings:
        message = (
            f"❗ Overdue Borrowing Alert!\n\n"
            f"👤 User: {borrowing.user.email}\n"
            f"📖 Book: {borrowing.book.title}\n"
            f"📅 Expected Return: {borrowing.expected_return_date}\n"
            f"📆 Borrowed On: {borrowing.borrowing_date}"
        )
        send_telegram_message(message)
