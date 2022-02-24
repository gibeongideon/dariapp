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
    C2BTransactionForm,
    CashTransferForm,
)
from users.models import User


@login_required(login_url="/user/login")
def mpesa_deposit(request):
    print("mpesa_deposit_TO:", request.user)
    form = C2BTransactionForm()
    if request.method == "POST":
        data = {}
        data["phone_number"] = request.user.phone_number
        data["amount"] = request.POST.get("amount")
        # form = C2BTransactionForm(data=request.POST)
        form = C2BTransactionForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("/account/mpesa_deposit/")
            
       

    trans_logz = CashDeposit.objects.filter(user=request.user).order_by("-id")[:10]


    return render(
        request,
        "account/mp_deposit.html",
        {
            "form": form,
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
    refer_credit = RefCredit.objects.filter(user=request.user).order_by("-created_at")

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
            pass

        data["recipient"] = recipient
        data["amount"] = request.POST.get("amount")
        form = CashTransferForm(data=data)
        if form.is_valid():
            form.save()

        if form.errors:
            pass
            # return redirect('/')#sError For TODO
    trans_logz = CashTransfer.objects.filter(sender=request.user).order_by("-id")[:10]

    return render(
        request, "account/cash_trans.html", {"form": form, "trans_logz": trans_logz}
    )


@login_required(login_url="/user/login")
def process_payment(request):
    amount = float(request.session['paypal_deposit_amount'])
    # print(amount)
    host =settings.SITE_DOMAIN  # 
    try:
        currency=Currency.objects.get(name="USD")
    except Currency.DoesNotExist:
        Currency.objects.create(name="USD",rate=100) 
        currency=Currency.objects.get(name="USD")

    try:
        dlatest=CashDeposit.objects.filter(user=request.user).latest('id')
        if dlatest.amount== amount:
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
        'item_name': 'DariPlay-Deposit',
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

