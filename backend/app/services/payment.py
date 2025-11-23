"""Payment processing with Stripe"""
import stripe
from typing import Optional
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else None


class PaymentService:
    """Service for handling payments"""

    @staticmethod
    async def create_payment_intent(
        amount: float,
        currency: str = "USD",
        description: str = "",
        metadata: dict = None
    ):
        """Create a Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                description=description,
                metadata=metadata or {},
            )
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
                "status": intent.status,
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Payment processing error: {str(e)}")

    @staticmethod
    async def confirm_payment(payment_intent_id: str):
        """Confirm a payment intent"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "status": intent.status,
                "amount": intent.amount / 100,
                "currency": intent.currency.upper(),
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Payment confirmation error: {str(e)}")

    @staticmethod
    async def create_checkout_session(
        amount: float,
        currency: str,
        success_url: str,
        cancel_url: str,
        metadata: dict = None
    ):
        """Create a Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'unit_amount': int(amount * 100),
                        'product_data': {
                            'name': 'Donation',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {},
            )
            return {
                "session_id": session.id,
                "url": session.url,
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Checkout session error: {str(e)}")

    @staticmethod
    async def create_subscription(
        customer_email: str,
        amount: float,
        currency: str,
        interval: str = "month"
    ):
        """Create a recurring subscription"""
        try:
            # Create or get customer
            customers = stripe.Customer.list(email=customer_email, limit=1)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(email=customer_email)

            # Create price
            price = stripe.Price.create(
                unit_amount=int(amount * 100),
                currency=currency.lower(),
                recurring={"interval": interval},
                product_data={"name": "Recurring Donation"},
            )

            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price.id}],
            )

            return {
                "subscription_id": subscription.id,
                "customer_id": customer.id,
                "status": subscription.status,
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Subscription creation error: {str(e)}")

    @staticmethod
    async def cancel_subscription(subscription_id: str):
        """Cancel a recurring subscription"""
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return {"status": subscription.status}
        except stripe.error.StripeError as e:
            raise Exception(f"Subscription cancellation error: {str(e)}")

    @staticmethod
    async def handle_webhook(payload: bytes, signature: str):
        """Handle Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )

            # Handle different event types
            if event.type == 'payment_intent.succeeded':
                payment_intent = event.data.object
                return {"event": "payment_succeeded", "data": payment_intent}
            elif event.type == 'payment_intent.payment_failed':
                payment_intent = event.data.object
                return {"event": "payment_failed", "data": payment_intent}
            elif event.type == 'customer.subscription.created':
                subscription = event.data.object
                return {"event": "subscription_created", "data": subscription}
            elif event.type == 'customer.subscription.deleted':
                subscription = event.data.object
                return {"event": "subscription_cancelled", "data": subscription}

            return {"event": event.type, "data": event.data.object}
        except Exception as e:
            raise Exception(f"Webhook processing error: {str(e)}")
