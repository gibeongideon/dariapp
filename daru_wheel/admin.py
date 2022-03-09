from django.contrib import admin
from .models import (
    Stake,
    Selection,
    OutCome,
    Selection,
    DaruWheelSetting,
    CashStore,
    Contact
)

class DaruWheelSettingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "refer_per",
        "per_to_keep",
        "min_bet",
        "win_algo",
        "trial_algo",
        "big_win_multiplier",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_editable = (
        "refer_per",
        "per_to_keep",
        "win_algo",
        "trial_algo",
        "big_win_multiplier",
        "min_bet",
    )


admin.site.register(DaruWheelSetting, DaruWheelSettingAdmin)


class SelectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "odds",
        "name",
        "selection_id_list",
        "selection_verbose_list",
        "created_at",
        "updated_at",
    )
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("id", "odds")


admin.site.register(Selection, SelectionAdmin)


class StakeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "marketselection",
        "amount",
        "win_multiplier",
        "expected_win_amount",
        "bet_on_real_account",
        "spinx",
        "spinned",
        "stake_placed",
        "has_record",
        "bet_status",
        "active_spins",
        "this_user_has_cash_to_bet",
        "created_at",
        "updated_at",
    )

    list_display_links = ("user",)
    search_fields = ("user",)
    list_filter = ("user", "marketselection","spinx","bet_on_real_account","spinned", "created_at")
    readonly_fields = ('spinx',)



admin.site.register(Stake, StakeAdmin)


class OutComeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stake",
        "closed",
        "give_away",
        "selection",
        "result",
        "pointer",
        "win_multiplier",        
        "real_bet",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id",)
    readonly_fields = ("closed", "result", "pointer")
    # list_editable = (
    #     "result",
    # )

admin.site.register(OutCome, OutComeAdmin)


class CashStoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "give_away",
        "to_keep",
    )

    list_display_links = ("id",)
    # readonly_fields = ('closgive_away',)


admin.site.register(CashStore, CashStoreAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cmail",
        "message",
    )

    list_display_links = ("id",)


admin.site.register(Contact, ContactAdmin)