import json
import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import PaymentSerializer
from ...models import PaymentModel
from cart.models import Cart


class PaymentRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_cart = Cart.objects.get(user=user)
        amount = user_cart.total_price
        data = {
            "amount": amount,
        }
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
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
            result = response.json()
            payments_status = result['Status']
            if payments_status in [100, 101]:
                # Save payment to the database
                PaymentModel.objects.create(
                    user=request.user,
                    amount=amount,
                    authority=result['Authority'],
                )
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
