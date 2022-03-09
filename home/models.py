from django.db import models


def filter_html_elements(content):
    #TODO
    return content


class Contact(models.Model):
    cmail =  models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "d_contact_us"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.message=filter_html_elements(self.message)#avoid XSS attack 
            super().save(*args, **kwargs)
        else:
            return    