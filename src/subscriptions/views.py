import stripe
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import CreateCheckoutSerializer
from rest_framework import status
from auth_ex.models import User


class CreateCheckoutSession(APIView):

    def post(self, request):
        try:

            serializer = CreateCheckoutSerializer(data=request.data)
            if serializer.is_valid():
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price': request.data.get('price_id'),
                            'quantity': 1,
                        },
                    ],
                    client_reference_id=request.user.pk,
                    mode='subscription',
                    success_url=settings.STRIPE_CHECKOUT_SUCCESS_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=settings.STRIPE_CHECKOUT_CANCEL_URL + '?canceled=true',
                )

                return Response(checkout_session, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomerPortal(APIView):

    def post(self, request):
        portalSession = stripe.billing_portal.Session.create(
            customer=request.user.customer_id,
            return_url=settings.STRIPE_CHECKOUT_RETURN_URL,
        )

        return Response({
            "url": portalSession.url
        }, status=200)


class GetPlans(APIView):

    def get(self, request):
        prices = stripe.Price.list()

        return Response(prices, status=200)


class Webhook(APIView):
    webhook_secret = settings.STRIPE_WEBHOOK_KEY

    def post(self, request):

        actions = {
            'checkout.session.completed': self.checkout_session_completed,
        }

        if self.webhook_secret:
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body, sig_header=signature, secret=self.webhook_secret)
                data = event['data']
            except Exception as e:
                return e

            event_type = event["type"]
            map_actions = actions.get(event_type)

            if map_actions:
                map_actions(data["object"])
                return Response({"status": "success"})

            return Response(
                {"error": f"Error placed in {event_type}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def checkout_session_completed(self, data):
        user_id = data.get('client_reference_id')
        customer_id = data.get('customer')

        User.objects.filter(pk=user_id).update(
            customer_id=customer_id
        )
