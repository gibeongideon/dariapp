from django import forms
from .models import Stake,Contact

class IstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("user", "marketselection","spinx", "amount", "bet_on_real_account")
        
class XstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("user", "amount","spinx", "bet_on_real_account")        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("cmail","message")        
