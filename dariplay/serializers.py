from .models import Match, Market, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Choice
            fields = ("name","odds","results")


class MarketSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many =True ,read_only =True)
    class Meta:
        model = Market
        fields = ('name','choices')

class MatchSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many =True ,read_only =True)
    class Meta:
        model = Match
        fields = ("code","home","away","markets")

