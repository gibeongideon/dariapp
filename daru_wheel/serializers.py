from .models import Stake
from rest_framework import serializers


class StakeSerializer(serializers.ModelSerializer):
    """
    A Stake serializer to return the Stake details
    """
    class Meta:
        model = Stake
        #fields = ('__all__')
        fields = ("user", "marketselection","spinx", "amount", "bet_on_real_account")
