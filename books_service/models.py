from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Daily rental fee in $USD"
    )
    inventory = models.PositiveIntegerField(
        help_text="Number of available copies of this book in the library"
    )
    cover = models.CharField(
        max_length=10, choices=CoverType.choices, default=CoverType.HARD
    )
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"
