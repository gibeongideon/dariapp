from django.db import models
from home.models import TimeStamp
from django.conf import settings
class Match(TimeStamp):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )#unique
    home = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    away = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.home}:{self.away}"


class MarketName(TimeStamp):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"MarketName:{self.name}"
class Market(TimeStamp):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="markets",
        blank=True,
        null=True,
    )
    name =  models.ForeignKey(
        MarketName,
        on_delete=models.CASCADE,
        related_name="markets",
        blank=True,
        null=True,
    )
   
    def __str__(self):
        return f"{self.match}-{self.name}"
        
    class Meta:
        unique_together=('match','name')



class Choice(TimeStamp):
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name="choices",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    odds = models.FloatField(default=0, blank=True, null=True)
    results= models.BooleanField(default=None, blank=True, null=True)###
    class Meta:
        unique_together=('market','name')


class BetList(TimeStamp):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )#unique


    def total_odds(self):
        pass#TODO

    def status(self):
        pass#TODO

    def __str__(self):
        return f"betlist:{self.code}"


class Bet(TimeStamp):    
    choice = models.OneToOneField(
        Choice,
        on_delete=models.CASCADE,
        related_name="clstakes",
        blank=True,
        null=True,
    )

    status= models.BooleanField(default=None, blank=True, null=True)###

    betlist = models.OneToOneField(
        BetList,
        on_delete=models.CASCADE,
        related_name="bettlists",
        blank=True,
        null=True,
    )  #

    
    def __str__(self):
        return f"stake:{self.amount} by:{self.user}"


class Stake(TimeStamp):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    betlist = models.ForeignKey(
        BetList,
        on_delete=models.CASCADE,
        related_name="betlists",
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        ("amount"), max_digits=12, decimal_places=2, default=50
    )
    
    def __str__(self):
        return f"place_stake:{self.amount} by:{self.user}on{self.betlist}"
