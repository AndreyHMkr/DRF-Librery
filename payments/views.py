import stripe
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from DRF_Library import settings
from payments.serializers import PaymentSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by payment status. Available values: PENDING, PAID, FAILED.",
        )
    ]
)
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.select_related("borrowing_id")
        return Payment.objects.select_related("borrowing_id").filter(
            borrowing_id__user=user
        )


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.select_related("borrowing_id")
        return Payment.objects.select_related("borrowing_id").filter(
            borrowing_id__user=user
        )


stripe.api_key = settings.STRIPE_SECRET_KEY


from rest_framework.response import Response
from rest_framework.views import APIView
from payments.models import Payment


class PaymentSuccessView(APIView):
    def get(self, request):
        session_id = request.GET.get("session_id")

        try:
            payment = Payment.objects.get(session_id=session_id)
            payment.status = Payment.Status.PAID
            payment.save()
        except Payment.DoesNotExist:
            return Response({"error": "Invalid session ID"}, status=400)

        return Response({"message": "Payment successful! ✅"})


class PaymentCancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment cancelled!"})
