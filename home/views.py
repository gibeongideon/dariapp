from django.shortcuts import redirect
from .forms import  ContactUsForm

def contact_us(request): 
    if request.method == "POST":
        cont_form = ContactUsForm(request.POST)
        if cont_form.is_valid():
            cont_form = cont_form.save(commit=False)
            if request.user.is_authenticated:
                cont_form.cmail = request.user.username 

            cont_form.save()
            return redirect('/')


    return redirect('/')
