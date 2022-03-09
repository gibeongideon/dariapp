from django import forms
from .models import Stake

class IstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("user", "marketselection","spinx", "amount", "bet_on_real_account")
        
class XstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("user", "amount","spinx", "bet_on_real_account")        
