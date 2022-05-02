from django.contrib import admin

from .models import (
    Account,
    Currency,
    RefCredit,
    RefCreditTransfer,
    CashDeposit,
    CashWithrawal,
    AccountSetting,
    CashTransfer,
    RegisterUrl,
    AccountAnalytic
)
class AccountSettingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "min_redeem_refer_credit",
        "auto_approve",
        "auto_approve_cash_trasfer",
        "withraw_factor",
        "created_at"
    )
    list_display_links = ("id",)
    search_fields = ("id",)
    list_editable = (
        "min_redeem_refer_credit",
        "auto_approve",
        "auto_approve_cash_trasfer",
        "withraw_factor",
       # "created_at"
    )


admin.site.register(AccountSetting, AccountSettingAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "user",
        "balance",
        "actual_balance",
        "withraw_power",
        "withrawable_balance",
        "withrawable_balance_usd",
        "refer_balance",
        "trial_balance",
        "cum_deposit",
        "cum_withraw",
        "c_loss",
        "active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("user_id","user")
    search_fields = ("id",)
    list_editable = (
        "balance",
        "actual_balance",
        "withraw_power",
        "refer_balance",
        "trial_balance",
        "cum_deposit",
        "cum_withraw",
      #  "created_at",
    )
    list_filter = ("user", "created_at", "updated_at")


admin.site.register(Account, AccountAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "rate",
        "created_at",
        "updated_at",
    )
    # list_display_links = ('',)
    search_fields = ("name",)
    list_editable = ("name", "rate")
    # readonly_fields =()


admin.site.register(Currency, CurrencyAdmin)


class RefCreditAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "user",
        "amount",
        "credit_from",
        "current_bal",
        "approved",
        "closed",
        "has_record",
        "created_at",
        "updated_at",
    )
    list_display_links = ("user_id",)
    search_fields = ("user_id",)
    list_editable = ("approved",)


admin.site.register(RefCredit, RefCreditAdmin)


class RefCreditTransferAdmin(admin.ModelAdmin):
    list_display = ("id","user_id", "user", "amount", "succided", "created_at", "updated_at")
    list_display_links = ("user_id",)
    search_fields = ("user_id",)
    # list_editable = ('approved',)

    list_filter = ("user","succided" ,"created_at", "updated_at")


admin.site.register(RefCreditTransfer, RefCreditTransferAdmin)
class CashDepositAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "deposited",
        "status",
        "deposit_type",
        "has_record",
        "amount",
        "tokens",
        "currency",
        "current_bal",
        "created_at",
        "updated_at",
    )
    list_display_links = ("user",)
    search_fields = ("amount",)
    list_filter = (
        "user",
        "currency",
        "deposit_type",
        "deposited",)
    readonly_fields = (
        "deposited",
        "has_record",
        "current_bal",
        "created_at",
        "updated_at",
    )
    list_editable = (
        "deposit_type",
        "tokens",

    )

admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "active",
        "previus_withrawals_is_incomplete",
        "cancelled",
        "approved",
        "withrawned",
        "withraw_status",
        "withr_type",
        "confirmed",
        "has_record",
        "amount",
        "tokens",
        "currency",
        "user_account",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id","amount",)
    search_fields = ("user",)
    list_filter = ("user", "approved", "cancelled","confirmed","withr_type","currency", "active","created_at","updated_at",)
    readonly_fields = (
        "withrawned",
        "has_record",
        "active",
        "user_account",
        "created_at",
        "updated_at",
    )
    list_editable = ("approved", "cancelled","confirmed","tokens")


admin.site.register(CashWithrawal, CashWithrawalAdmin)


class CashTransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "recipient",
        "amount",
        "approved",
        "cancelled",
        "success",
        "created_at",
        "updated_at",
        "active"
    )
    list_display_links = ("id",)
    list_filter = ("sender","recipient", "approved", "cancelled","active")
    list_editable = ("amount", "approved","cancelled")


admin.site.register(CashTransfer, CashTransferAdmin)
admin.site.register(RegisterUrl)


class AccountAnalyticAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gain",
        "t_bal",
        "t_wit",
        "t_in",
        "t_out",
        "diffe",
        "flag","status_flag","c_bal","wit_amount","all_in","all_out",
        # "current_flag",
        "created_at", "updated_at")
    list_display_links = ("id",)
    # list_editable = ('',)


admin.site.register(AccountAnalytic, AccountAnalyticAdmin)
