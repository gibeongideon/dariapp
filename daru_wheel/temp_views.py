from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import logout
from users.models import User
from .forms import  IstakeForm
from .models import Stake

AnonymousUser=AnonymousUser()


# @login_required(login_url="/user/login")
def spin(request,*args,**kwargs):
    
    refercode = kwargs.get('refer_code')
    try:        
        User.objects.get(code=refercode)
        if request.user.is_authenticated:
            logout(request)
        request.session['ref_code']=refercode
    except User.DoesNotExist:
        pass
    
    if request.user!=AnonymousUser:
        print('USER')
        print(request.user) 
        
        trans_logz = Stake.objects.filter(
            user=request.user
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
        "spins": spins,
    }

    return render(request, "daru_wheel/ispind.html", context)
    # return render(request, "daru_wheel/ispind.html")



@login_required(login_url="/user/login")
def stakes(request):
    trans_logz = Stake.objects.filter(
        user=request.user
    ).order_by("-created_at")[:20]


    context = {
        "trans_logz": trans_logz,
        }

    return render(request, "daru_wheel/stakes.html", context)
