from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import StakeForm, IstakeForm
from .models import Stake, Selection
import json
AnonymousUser=AnonymousUser()


# @login_required(login_url="/user/login")
def spin(request):

    if request.user!=AnonymousUser:
        print('USER')
        print(request.user) 
        
        trans_logz = Stake.objects.filter(
            user=request.user,
            market=None,
            has_market=False
            ).order_by("-created_at")[:2]
    else:
        trans_logz=[]

    if request.method == "POST":
        stake_form = IstakeForm(request.POST)
        if stake_form.is_valid():
            stake = stake_form.save(commit=False)
            stake.user = request.user
            stake.save()
            # return redirect('/')
    else:
        stake_form = IstakeForm()
        # print(stake_form.errors)

    if request.user!=AnonymousUser:
        spins = len(Stake.unspinned(request.user.id))
    else:
        spins=0
    

    context = {
        "user": request.user,
        "stake_form": stake_form,
        "trans_logz": trans_logz,
        # "spins": spins,
    }

    return render(request, "daru_wheel/ispind.html", context)
    # return render(request, "daru_wheel/ispind.html")



@login_required(login_url="/user/login")
def spine(req):

    tmpl_vars = {
        "trans_logz": Stake.objects.filter(user=req.user).order_by("-created_at")[:12],
        "form": IstakeForm(),
        "spins": Stake.unspinned(req.user.id),
    }

    return render(req, "daru_wheel/ispin.html", tmpl_vars)


@login_required(login_url="/user/login")
def spin_it(request):
    if request.method == "POST":
        market_id = request.POST.get("marketselection")
        # print(f"ARKETTT_ID:{market_id}")
        marketselection = Selection.objects.get(id=1)  # market_id)
        # request.POST.get('marketselection')
        amount = request.POST.get("amount")
        # print("AOOOO")
        # print(amount)

        bet_on_real_account = request.POST.get("bet_on_real_account")
        # print("REL_FAK")
        # print(bet_on_real_account)
        if bet_on_real_account == "on" or True:
            bet_on_real_account = True
        else:
            bet_on_real_account = False

        # print("REL_FAK2")
        # print(bet_on_real_account)
        response_data = {}

        stake = Stake(
            marketselection=marketselection,
            amount=amount,
            bet_on_real_account=True,
            user=request.user,
        )
        stake.save()

        response_data["created_at"] = stake.created_at.strftime("%B %d, %Y %I:%M %p")
        response_data["marketselection"] = stake.marketselection.name
        response_data["amount"] = stake.amount
        response_data["bet_status"] = stake.bet_status()
        response_data["bet_on_real_account"] = stake.bet_on_real_account

        return JsonResponse(response_data)

    return JsonResponse({"Error": "Postin Error"})



@login_required(login_url="/user/login")
def stakes(request):
    trans_logz = Stake.objects.filter(
        user=request.user, market=None, has_market=False
    ).order_by("-created_at")[:20]


    context = {
        "trans_logz": trans_logz,
        }

    return render(request, "daru_wheel/stakes.html", context)
