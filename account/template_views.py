from paypal.standard.forms import PayPalPaymentsForm
from django.conf import  settings
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import (
    RefCredit,
    CashWithrawal,
    Account,
    AccountSetting,
    CashDeposit,
    CashTransfer,
    Currency
)
from .forms import (
    CashWithrawalForm,
    ReferTranferForm,
    CashTransferForm,
)
from users.models import User
from mpesa_api.core.mpesa import Mpesa
import logging

logger = logging.getLogger(__name__)

@login_required(login_url="/user/login")
def mpesa_deposit(request):
    if request.method == "POST":
        phone_number = request.user.phone_number
        amount = request.POST.get("amount")
        try:
            Mpesa.stk_push(
                phone_number,
                amount,
                account_reference=f"Pay Darius Option KSH {amount} for account of {request.user.username} using mobile no {phone_number}",
                is_paybill=False,
            )
        except Exception  as e:
            logger.exception(e)
 
       
    trans_logz = CashDeposit.objects.filter(user=request.user).order_by("-id")[:10]

    return render(
        request,
        "account/mp_deposit.html",
        {
            "trans_logz": trans_logz,

        },
    )



@login_required(login_url="/user/login")
def refer_credit(request):
    form = ReferTranferForm()
    if request.method == "POST":
        data = {}
        data["user"] = request.user
        data["amount"] = request.POST.get("amount")
        form = ReferTranferForm(data=data)
        if form.is_valid():
            form.save()
           
    min_wit, _ = AccountSetting.objects.get_or_create(id=1)
    min_wit = min_wit.min_redeem_refer_credit
    account_bal = float(Account.objects.get(user=request.user).balance)
    refer_bal = float(Account.objects.get(user=request.user).refer_balance)
    refer_credit = RefCredit.objects.filter(user=request.user).order_by("-created_at")[:10]

    return render(
        request,
        "account/refer_credit.html",
        {
            "form": form,
            "refer_credit": refer_credit,
            "account_bal": account_bal,
            "refer_bal": refer_bal,
            "min_wit": min_wit,
            # 're_to_wit':re_to_wit
        },
    )


@login_required(login_url="/user/login")
def mpesa_withrawal(request):
    uf = Account.objects.get(user=request.user)
    try:
        currency=Currency.objects.get(name="KSH")
    except Currency.DoesNotExist:
        Currency.objects.create(name="KSH",rate=1) ###
        currency=Currency.objects.get(name="KSH")
    form = CashWithrawalForm()
    if request.method == "POST":
        data = {}
        data["user"] = request.user
        data["amount"] = request.POST.get("amount")
        data["withr_type"] = 'mpesa'
        data["currency"] = currency
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("/account/mpesa_withrawal")#
       
    trans_logz = CashWithrawal.objects.filter(user=request.user,withr_type='mpesa').order_by("-id")[:10]

    return render(
        request,
        "account/mpesa_withrawal.html",
        {"form": form, "trans_logz": trans_logz,"uf": uf},
    )



@login_required(login_url="/user/login")
def paypal_withrawal(request):
    uf = Account.objects.get(user=request.user)
    try:
        currency=Currency.objects.get(name="USD")
    except Currency.DoesNotExist:
        Currency.objects.create(name="USD",rate=100) ###
        currency=Currency.objects.get(name="USD")


    form = CashWithrawalForm()
    if request.method == "POST":
        data = {}
        data["user"] = request.user
        data["amount"] = request.POST.get("amount")
        data["withr_type"] = 'paypal'
        data["currency"] = currency
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("/account/paypal_withrawal/")#
       
    trans_logz = CashWithrawal.objects.filter(user=request.user,withr_type='paypal').order_by("-id")[:10]

    return render(
        request,
        "account/paypal_withrawal.html",
        {"form": form, "trans_logz": trans_logz,"uf": uf},
    )


def format_mobile_no(mobile):
    mobile = str(mobile)
    if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
        return "254" + mobile[1:]
    if mobile.startswith("254") and len(mobile) == 12:
        return mobile
    if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
        return "254" + mobile
    return mobile


@login_required(login_url="/user/login")
def cash_trans(request):
    form = CashTransferForm()
    if request.method == "POST":
        data = {}
        data["sender"] = request.user
        recipient = request.POST.get("recipient")

        try:
            recipient = User.objects.get(username=recipient.strip())
        except Exception:
            try:
                recipient=format_mobile_no(recipient)
                recipient = User.objects.get(phone_number=recipient.strip())
            except:
                pass    

        data["recipient"] = recipient
        data["amount"] = request.POST.get("amount")
        form = CashTransferForm(data=data)
        if form.is_valid():
            form.save()

        if form.errors:
            pass
            # return redirect('/')#sError For TODO
    trans_logz0 = CashTransfer.objects.filter(sender=request.user).order_by("-id")[:10]
    trans_logz1 = CashTransfer.objects.filter(recipient=request.user).order_by("-id")[:10]
    trans_logz=list(trans_logz0)+list(trans_logz1)
    return render(
        request, "account/cash_trans.html", {"form": form, "trans_logz": trans_logz}
    )

@login_required(login_url="/user/login")
def stop_cash_trans(request):
    if request.method == "POST":
        pk= request.POST.get("pk")
        ct=CashTransfer.objects.get(id=pk)
        if not ct.cancelled==True and not ct.success==True:
            CashTransfer.objects.filter(pk=pk).update(cancelled=True,active=False,success=False)
            return redirect("/account/cash_trans/")
        return redirect("/account/cash_trans/") 
            



@login_required(login_url="/user/login")
def process_payment(request):
    amount = float(request.session['paypal_deposit_amount'])
    #host =settings.SITE_DOMAIN  # 
    host = request.get_host()
    try:
        currency=Currency.objects.get(name="USD")
    except Currency.DoesNotExist:
        Currency.objects.create(name="USD",rate=100) 
        currency=Currency.objects.get(name="USD")

    try:
        dlatest=CashDeposit.objects.filter(user=request.user).latest('id')
        if dlatest.amount== amount and dlatest.confirmed!=True:
            depo=dlatest
        else:
            depo=CashDeposit.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                deposit_type="Paypal",)
    except:
        depo=CashDeposit.objects.create(
            user=request.user,
            amount=amount,
            currency=currency,
            deposit_type="Paypal",)                   


    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{amount}',
        'item_name': 'Deposit to {request.user.username} account at Dariplay',
        'invoice': f'{depo.id}',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}/'.format(host),
        'cancel_return': 'http://{}/account/paypal/checkout'.format(host),
  
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(
        request,
        'account/paypal/process_payment.html',
        {'amount': amount, 'form': form})


def checkout(request):
    if request.method == 'POST':
        request.session['paypal_deposit_amount']=request.POST.get("amount")
        return redirect('/account/paypal/process-payment')
    else:
        return render(request, 'account/paypal/checkout.html')


@csrf_exempt
def payment_done(request):
    return render(request, 'account/paypal/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'account/paypal/payment_cancelled.html')

