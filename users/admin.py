from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Password


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

    list_display_links = ("id","username")
    search_fields = ("phone_number","email","username","referer_code","email")
    ordering = ("id",)

    list_filter = ("username","phone_number","referer_code","last_login","active",)

    list_editable = (
        "phone_number",
        "code",
        "referer_code",
        "email"
    )
    readonly_fields = ("password",)


admin.site.register(User, DuserAdmin)


class PasswordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "password",
        "created_at",
        "updated_at"
    )

    list_display_links = ("id","username","created_at","updated_at")
    search_fields = ("username","Password",)
    ordering = ("id",)

    list_filter = ("username","created_at")


    readonly_fields = ("password","username")


admin.site.register(Password, PasswordAdmin)