from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse,HttpResponseNotFound
from django import template
from random import randint
from account.models import Checkout
from account.forms import CheckoutForm
from .forms import SubscriberForm

# @login_required(login_url="/user/login")
def homepage(request):
    # print(request.user)
    spin_players_no = randint(800, 1200)
    return render(request, "home/home_page.html",{
        "spin_players_no": spin_players_no})


# @login_required(login_url="user/login")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split("/")[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("error-404.html")
        return HttpResponse(html_template.render(context, request))

    # except:

    #     html_template = loader.get_template("error-500.html")
    #     return HttpResponse(html_template.render(context, request))


@login_required(login_url="/user/login")
def deposit_withraw(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.email = request.user.email
            form.save()
            # cleaned_data = form.cleaned_data
            return redirect('/account/process-payment')
    else:
        form = CheckoutForm()
        return render(request, 'home/deposit_withraw.html', locals())


# @login_required(login_url="/user/login")
def affiliate(request):
    return render(request, "home/affiliate.html")




# def subscribe(request):
#     if request.method == "POST":
#         form = SubscriberForm(request.POST)
#         if form.is_valid():
#              form.save()
#         return redirect('/spin')
#     else:
#         sub_form = SubscriberForm()

#     context = {
#         "form": form,
#     }

#     # return render(request, "home/home_page.html", context)
