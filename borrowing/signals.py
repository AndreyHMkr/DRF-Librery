from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from borrowing.models import Borrowing
from telegram_notifications.utils.telegram import send_telegram_message


@receiver(post_save, sender=Borrowing)
def send_borrowing_created_notification(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    book = instance.book
    message = (
        f"📚 <b>New Borrowing Created</b>\n"
        f"User: {user.email}\n"
        f"Book: <i>{book.title}</i>\n"
        f"Borrow date: {instance.borrowing_date}\n"
        f"Expected return: {instance.expected_return_date}"
    )

    send_telegram_message(message)


@receiver(post_save, sender=Borrowing)
def send_borrowing_returned_notification(sender, instance, created, **kwargs):
    if created or not instance.actual_return_date:
        return
    if (
        instance.actual_return_date
        and instance.actual_return_date == timezone.now().date()
    ):
        message = (
            f"✅ <b>Book is returned</b>\n"
            f"User: {instance.user.email}\n"
            f"Book: <i>{instance.book.title}</i>\n"
            f"Data of returned: {instance.actual_return_date}"
        )
        send_telegram_message(message)
