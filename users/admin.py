from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class DuserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "phone_number",
        "email",
        "first_name",
        "last_name",
        "code",
        "referer_code",
        "last_login",
        "active",
        "referees_no",
        "referal_link",
    )

    list_display_links = ("id",)
    search_fields = ("phone_number","username","referer_code","email")
    ordering = ("id",)

    list_filter = ("username","phone_number","referer_code", "active",)

    list_editable = (
        "phone_number",
        "code",
        "referer_code",
    )
    readonly_fields = ("password",)


admin.site.register(User, DuserAdmin)
