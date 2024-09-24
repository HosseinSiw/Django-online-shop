import json
import requests

from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from .serializers import PaymentSerializer
from ...models import PaymentModel
from cart.models import Cart


"""
This file contains views for payment, both request to pay and validation.
"""


class PaymentRequestView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        """
        This provided view is for send a payment request to zarinpal API, But it currently has error due to
        MISS-CONFIGURATION of ZARINPAL Client, config it as your own in settings.py file at the root of the project.
        :param request:
        :param args:
        :param kwargs:
        :return: A Response object
        """
        user = request.user
        user_cart = Cart.objects.get(user=user)
        amount = user_cart.total_price
        shipping_address = request.data.get("shipping_address")
        data = {
            "shipping_address": shipping_address,
        }
        Order.objects.create(
            cart=user_cart,
            shipping_address=shipping_address,
            status="P",
        )
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            zarinpal_request_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
            if not settings.ZARINPAL_SANDBOX:
                zarinpal_request_url = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"

            data = {
                "MerchantID": settings.ZARINPAL_MERCHANT_ID,
                "Amount": int(amount * 10),
                "Description": "Payment description",
                "CallbackURL": settings.ZARINPAL_CALLBACK_URL,
            }
            header = {
                "Content-Type": "application/json",
            }
            response = requests.post(zarinpal_request_url, json=json.dumps(data,), headers=header)
            # print(response)  # Debugging purposes
            result = response.json()
            payments_status = result['Status']
            if payments_status in [100, 101]:
                # Save payment to the database
                PaymentModel.objects.create(
                    user=request.user,
                    amount=amount,
                    authority=result['Authority'],
                )
                order = Order.objects.get(user=request.user, status="S")
                order.status = "S"  # S represents Shipped status
                order.save()
                return Response({
                    "message": "Payment initiated",
                    "authority": result['Authority'],
                    "payment_url": f"https://sandbox.zarinpal.com/pg/StartPay/{result['Authority']}"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Payment request failed",
                    "status_code": result['Status']
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        payment_status = request.GET.get('Status')

        try:
            payment = PaymentModel.objects.get(authority_id=authority)
            if payment_status == "OK":
                zarinpal_verify_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
                if not settings.ZARINPAL_SANDBOX:
                    zarinpal_verify_url = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
                data = {
                    "MerchantID": settings.ZARINPAL_MERCHANT_ID,
                    "Authority": authority,
                    "Amount": int(payment.amount * 10),
                }

                response = requests.post(zarinpal_verify_url, json=data)
                result = response.json()
                if result['Status'] == "OK":
                    payment.status = "successful"
                    payment.save()
                    user = request.user
                    user_cart = Cart.objects.get(user=user)
                    Order.objects.create(
                        user=user,
                        cart=user_cart,
                    )
                    return Response({
                        "message": "Payment successful",
                        "ref_id": result['RefID']
                    }, status=payment_status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Payment verification failed",
                        "status_code": result['Status']
                    }, status=payment_status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "error": "Payment cancled by user",
                }, status=payment_status.HTTP_400_BAD_REQUEST)
        except PaymentModel.DoesNotExist:
            return Response({
                "error": "Invalid Payment",
            }, status=payment_status.HTTP_404_BAD_REQUEST)
