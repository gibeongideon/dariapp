from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
import os
from .models import Account, CashWithrawal, Currency
# import json
import random
import string
from .paypal_client import PayPalClient,CreatePayouts
from paypalpayoutssdk.payouts import PayoutsPostRequest


from django.contrib.auth.decorators import login_required





@login_required(login_url="/user/login")
def paypal_payout(request):
    if request.method == "POST":
        amount=float(request.POST['amount'])
        try:
            currency=Currency.objects.get(name="USD")
        except Currency.DoesNotExist:
            Currency.objects.create(name="USD",rate=100) ###
            currency=Currency.objects.get(name="USD")        

        try:
            create_response = CreatePayouts(str(amount), request.user.email).create_payouts(True)
        except Exception as e:
            print('paypal_WIT',e) #debug  
            return render(request, "account/paypal/payment.html", {"msg": 'Failed try again.Connection issue'})


        if int(create_response.status_code) == 201:

            CashWithrawal.objects.create(
                user=request.user,
                amount=float(amount),
                currency=currency,
                approved=True,
                )

            msg=f'{amount} withrawned successfully.Check your paypal balance'       

            return render(request, "account/paypal/payment.html", {"msg": msg})
        msg=f'{amount} NOT withrawned successfully.Try again'    
        return render(request, "account/paypal/payment.html", {"msg": msg})    
    else:
        try:
            uf = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            uf = Account(user=request.user, balance=0).save()
        return render(request, "account/paypal/payment.html", {
            "uf": uf
        })
