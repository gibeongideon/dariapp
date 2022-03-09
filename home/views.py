from django.shortcuts import redirect
from .forms import  ContactForm

def contact(request): 
    if request.method == "POST":
        cont_form = ContactForm(request.POST)
        if cont_form.is_valid():
            cont_form = cont_form.save(commit=False)
            if request.user.is_authenticated:
                cont_form.cmail = request.user.username 

            cont_form.save()
            return redirect('/')
    else:
        cont_form = ContactForm()

    return redirect('/')
