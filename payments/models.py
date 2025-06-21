from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
    )
    borrowing_id = models.ForeignKey(
        "borrowing.Borrowing",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.status}) for borrowing {self.borrowing_id}"
