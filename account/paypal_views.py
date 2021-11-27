from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import os
from .models import Account,CashDeposit, Currency
import json
import random
import string
from .paypal_client import DPayPalClient
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp.serializers.json_serializer import Json
from paypalhttp.http_error import HttpError
from paypalhttp.encoder import Encoder
from django.conf import settings

# Creating an environment
client_id = settings.PAYPAL_CLIENT_ID

environment = SandboxEnvironment(client_id=client_id, client_secret=settings.PAYPAL_CLIENT_SECRET)
client = PayPalHttpClient(environment)



class CreatePayouts(DPayPalClient):

    """ Creates a payout batch with 5 payout items
    Calls the create batch api (POST - /v1/payments/payouts)
    A maximum of 15000 payout items are supported in a single batch request"""

    def __init__(self, amount, receiver):
        self.amount = amount
        self.receiver = receiver
        DPayPalClient.__init__(self)

    # @staticmethod
    def build_request_body(self, include_validation_failure = False):
        senderBatchId = str(''.join(random.sample(
            string.ascii_uppercase + string.digits, k=7)))
        amount = self.amount # if include_validation_failure else "1.00"
        return \
            {
                "sender_batch_header": {
                    "recipient_type": "EMAIL",
                    "email_message": "SDK payouts test txn",
                    "note": "Enjoy your Payout!!",
                    "sender_batch_id": senderBatchId,
                    "email_subject": "This is a test transaction from SDK"
                },
                "items": [{
                    "note": "Thanks for using dariplay!",
                    "amount": {
                        "currency": "USD",
                        "value": amount
                    },
                    "receiver": self.receiver,
                    "sender_item_id": "Test_txn_1"
                }]
            }

    def create_payouts(self, debug=False):
        request = PayoutsPostRequest()
        request.request_body(self.build_request_body(False))
        response = self.client.execute(request)

        if debug:
            print("Status Code: ", response.status_code)
            print("Payout Batch ID: " +
                  response.result.batch_header.payout_batch_id)
            print("Payout Batch Status: " +
                  response.result.batch_header.batch_status)
            print("Links: ")
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))

            # To toggle print the whole body comment/uncomment the below line
            #json_data = self.object_to_json(response.result)
            #print "json_data: ", json.dumps(json_data, indent=4)

        return response

# Create your views here.
def accept_payment(request):
    return render(request, "account/paypal/accept-payment.html",{"client_id":client_id})

@csrf_exempt # security issue
def payment_success(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))

        try:
            Account.objects.get(user=request.user)
            currency=Currency.objects.get(name="USD")
            CashDeposit.objects.create(user=request.user,amount=post_data["amount"],deposit_type='paypal',currency=currency)

        except Exception as e:
            print(e)
            print('paypal deposir_ISSUE!!')
            
            pass

        print(post_data)

        return JsonResponse({"success": True})

def paypal_payout(request):
    if request.method == "POST":
        create_response = CreatePayouts(str(float(request.POST['amount'])), request.user.username).create_payouts(True)
        if int(create_response.status_code) == 201:
            uf = Account.objects.get(user=request.user)
            uf.balance = uf.balance - float(request.POST['amount'])
            uf.save()
        return JsonResponse({"status code": create_response.status_code})
    else:
        try:
            uf = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            uf = Account(user=request.user, balance=0).save()
        return render(request, "account/paypal/payment.html", {
            "uf": uf
        })