from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from users.models import User
from .forms import  IstakeForm,XstakeForm
from .models import Stake
from home.models import UserStat
from  datetime import date


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
    
    if not request.user.is_anonymous:         
        trans_logz = Stake.objects.filter(
            user=request.user,
            spinx=False
            ).order_by("-created_at")[:2]
    else:
        trans_logz=[]

    if request.method == "POST":
        stake_form = IstakeForm(request.POST)
        if stake_form.is_valid():
            stake = stake_form.save(commit=False)
            stake.user = request.user
            spinx=False,
            stake.save()
    else:
        stake_form = IstakeForm()
    
    print(date.today())
    print("NOWWW")    
    
    try:
       UserStat.objects.get(id=1)
    except:
       UserStat.objects.create(id=1)
    #print(UserStat.objects.last())
    #user_sta=UserStat.objects.last()
    #print(user_sta.homepage_hits_login)
    #if date.today() !=UserStat.objects.last():
     #  pass
       
    userstat=UserStat.objects.last()

    if not request.user.is_anonymous:
        spins = len(Stake.unspinned(request.user.id))                         
        
        homepage_hits_login=userstat.homepage_hits_login+1
        userstat.homepage_hits_login=homepage_hits_login
        userstat.save()
    else:
        spins=0  
        
        homepage_hits_anonymous=userstat.homepage_hits_anonymous+1
        userstat.homepage_hits_anonymous=homepage_hits_anonymous
        userstat.save()
    
    context = {
        "user": request.user,
        "stake_form": stake_form,
        "trans_logz": trans_logz,
        "spins": spins,
    }

    return render(request, "daru_wheel/ispind.html", context)

# @login_required(login_url="/user/login")
def spinx(request,*args,**kwargs):    
    refercode = kwargs.get('refer_code')
    try:
        User.objects.get(code=refercode)
        if request.user.is_authenticated:
            logout(request)
        request.session['ref_code']=refercode
    except User.DoesNotExist:
        pass
    
    if not request.user.is_anonymous:    
        trans_logz = Stake.objects.filter(
            user=request.user,
            spinx=True
            ).order_by("-created_at")[:2]
    else:
        trans_logz=[]

    if request.method == "POST":
        stake_form = XstakeForm(request.POST)
        if stake_form.is_valid():
            stake = stake_form.save(commit=False)
            stake.user = request.user
            stake.spinx = True
            stake.save()
            #return redirect('/')
    else:
        stake_form = XstakeForm()
    try:
       UserStat.objects.get(id=1)
    except:
       UserStat.objects.create(id=1)
       
    userstat=UserStat.objects.last()
    if not request.user.is_anonymous:
        spins = len(Stake.unspinnedx(request.user.id))                         
        
        spinx_hits=userstat.spinx_hits+1
        userstat.spinx_hits=spinx_hits
        userstat.save()

    else:
        spins=0  
        
        spinx_hits_anonymous=userstat.spinx_hits_anonymous+1
        userstat.spinx_hits_anonymous=spinx_hits_anonymous
        userstat.save()
    
    context = {
        "user": request.user,
        "stake_form": stake_form,
        "trans_logz": trans_logz,
        "spins": spins,
    }
    return render(request, "daru_wheel/ispinx.html", context)
    

@login_required(login_url="/user/login")
def stakes(request):
    trans_logz = Stake.objects.filter(
        user=request.user
    ).order_by("-created_at")[:20]


    context = {
        "trans_logz": trans_logz,
        }

    return render(request, "daru_wheel/stakes.html", context)
