from django.contrib import admin

from borrowing.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "borrowing_date",
        "expected_return_date",
        "actual_return_date",
        "book",
        "user",
    )
