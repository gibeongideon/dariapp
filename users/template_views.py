from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views

from .models import User,Password
from .forms import SignUpForm





@login_required(login_url="/users/login")
def mine_users(request):
    mine_users = User.objects.filter(referer_code=request.user.code)

    return render(request, "users/mine_users.html", {"mine_users": mine_users})




class CustomLoginView(auth_views.LoginView):
    """Collect methods which extends django authentication functionality."""

    def form_valid(self, form):
        """Extend basic validation with user remember functionality.

        Check if remember checkbox was set by user and store session data
        in such case.
        """
        if self.request.POST.get("remember_me", None):
            self.request.session.set_expiry(60)
        return super().form_valid(form)


def register(request):
    """Responsible for validation and creation of new users.

    Check if all required inputs are filled, if password and
    password confirmation are equal, if user with posted username
    already not exists and then create new user with possible friend username
    or blank string. After succesed registration proceed authentication
    and redirect to index path, otherwise return error messages to source
    registration form.
    """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()#(commit=False)
            
            try:
                if request.session['ref_code']:
                    referer_code=str(request.session['ref_code'])  
            except Exception as e:
                referer_code=str(User.objects.get(id=1).code)#use_ref_wit_less_users_REFS_AL#TODO


            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            Password.objects.create(username=username,password=raw_password)    #privacy *****
            
            User.objects.filter(username=username).update(referer_code=referer_code)#NEDD_FIXX/Double_Job


            user = authenticate(username=username, password=raw_password)
            user.save()

            login(request, user)
            return redirect("/")
  
     
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
