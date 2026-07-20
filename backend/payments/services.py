from .models import Payment


class PaymentService:
    """
    Handles payment creation.
    """

    @staticmethod
    def create_payment(
        order,
        payment_method,
    ):

        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.total_amount,
        )

        return payment