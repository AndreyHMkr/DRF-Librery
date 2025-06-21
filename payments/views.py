from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from payments.models import Payment
from payments.serializers import PaymentSerializer


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
