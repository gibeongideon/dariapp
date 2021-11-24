from django.contrib import admin

from .models import BetList, Choice,Match,Market,Bet,Stake,MarketName


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "home",
        "away",
    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "code",
        "home",
        "away",
    )
admin.site.register(Match, MatchAdmin)


class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "match",
        "name",

    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "match",
        "name",

    )

admin.site.register(Market, MarketAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "market",
        "name",
        "odds",
        "results"
    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "market",
        "name",
        "odds",
        "results"
    )

admin.site.register(Choice, ChoiceAdmin)

admin.site.register(BetList)

admin.site.register(MarketName)

class BetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "choice",
        "status",
        "betlist",
    )
    list_display_links = ("id",)
    search_fields = ("id",)

admin.site.register(Bet, BetAdmin)



class StakeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "betlist",
        "amount",
    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "user",
        "betlist",
        "amount",
    )
admin.site.register(Stake, StakeAdmin)


