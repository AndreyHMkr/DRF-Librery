"""
URL configuration for DRF_Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books_service.views import BookViewSet
from borrowing.views import BorrowingViewSet
from payments.views import (
    PaymentListView,
    PaymentDetailView,
    PaymentSuccessView,
    PaymentCancelView,
)

router = DefaultRouter()
router.register("borrowing", BorrowingViewSet, basename="borrowing")
router.register("books", BookViewSet, basename="books")


urlpatterns = [
    path("api/user/", include("user.urls", namespace="user")),
    path("api/payments/", PaymentListView.as_view(), name="payment-list"),
    path("api/payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
    path("api/", include(router.urls)),
] + debug_toolbar_urls()
