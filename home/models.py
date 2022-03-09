from django.db import models


class Contact(models.Model):
    cmail =  models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "d_contact_us"