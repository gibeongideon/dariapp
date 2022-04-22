from django.contrib import admin
from django.contrib import admin
from .models import ContactUs,UserStat

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cmail",
        "message",
    )

    list_display_links = ("id",)


admin.site.register(ContactUs, ContactAdmin)

class UserStatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "homepage_hits_login",
        "homepage_hits_anonymous"

    )
    list_display_links = ("id",)


admin.site.register(UserStat, UserStatAdmin)
