from django.contrib import admin
from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cmail",
        "message",
    )

    list_display_links = ("id",)


admin.site.register(Contact, ContactAdmin)