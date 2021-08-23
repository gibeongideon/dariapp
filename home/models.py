from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,InlinePanel, MultiFieldPanel)
    
from wagtail.images.edit_handlers import ImageChooserPanel 
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel



from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        
class Subscriber(TimeStamp):
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return str(self.email)
    
       

class WebPa(TimeStamp):
    navbar_eder = models.CharField(
        max_length=100, default="Daru Wheel", blank=True, null=True
    )
    footer1 = models.CharField(
        max_length=100, default="Darius & Co.", blank=True, null=True
    )
    footer2_url = models.CharField(
        max_length=100,
        default="https://www.github.com/gibeongideon",
        blank=True,
        null=True,
    )
    footer3 = models.CharField(max_length=100, blank=True, null=True)
    header1 = models.CharField(
        max_length=100, default="Welcome to Daruwheel", blank=True, null=True
    )
    header2 = models.CharField(
        max_length=100, default="Play and Win Real Cash", blank=True, null=True
    )
    header3 = models.CharField(max_length=100, blank=True, null=True)
    header4 = models.CharField(max_length=100, blank=True, null=True)
    copyright_text = models.CharField(max_length=30, blank=True, null=True)

    mpesa_header_depo_msg = models.TextField(
        max_length=300,
        default="Enter amount and click send.Check M-pesa SMS send to your mobile NO you register with to confirm transaction.",
        blank=True,
        null=True,
    )
    share_info = models.TextField(
        max_length=300,
        default="Share the code to other people to get credit whenever they bet.Once someone register you will always get some credit whenever they place stake.Make sure they entered the code correctly when they signup.",
        blank=True,
        null=True,
    )



class HomePage(Page):
    
    # image0 = models.ImageField(upload_to='images/intro/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    # signature_01 = models.ImageField(upload_to='images/signature/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    intro_quote1 = models.CharField(default="Our quest to empower & change ",max_length=200, blank=True,null=True)
    intro_quote2 = models.CharField(default="every hustler's",max_length=200, blank=True,null=True)
    intro_quote3 = models.CharField(default=" life.",max_length=200, blank=True,null=True)

    body = RichTextField(blank=True)
#     latest_new_title = models.CharField(max_length=200, default='Latest News', blank=True,null=True)
    
    big_tittlea = models.CharField(max_length=250 ,blank=True,null=True)
#     join_tittleb = models.CharField(max_length=250 ,blank=True,null=True)
#     join_tittlec = models.CharField(max_length=250 ,blank=True,null=True)

    advert = models.ForeignKey(
        'home.Advert',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')
# 
    header = models.ForeignKey(
        'home.Header',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')

    footer = models.ForeignKey(
        'home.Footer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')        


    content_panels=Page.content_panels + [
        SnippetChooserPanel('advert'),
        SnippetChooserPanel('header'),
        SnippetChooserPanel('footer'),
        FieldPanel('body',classname = "full"),
        # FieldPanel('image0'),
        # FieldPanel('signature_01'),

        FieldPanel('big_tittlea'),


#         FieldPanel('intro_quote1'),
#         FieldPanel('intro_quote2'),
#         FieldPanel('intro_quote3'),

#         # InlinePanel('latestnewz',label="Latest News"),


    ]
    
    @property
    def spin_players_no(self):
        return 607







@register_snippet
class Advert(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return str(self.text)


@register_snippet
class Header(models.Model):
    faicon = models.ImageField(upload_to='images/faricon/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255,blank=True,null=True)
    logo = models.ImageField(upload_to='images/logo/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    logo1 = models.ImageField(upload_to='images/logo/%Y/%m/%d/',max_length=2000,blank=True ,null =True)

    

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
        FieldPanel('logo'),
        FieldPanel('logo1'),
        FieldPanel('faicon'),
        
    ]

    def __str__(self):
        return str(self.text)


@register_snippet
class Footer(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255, blank=True,null=True)
    logofooter = models.ImageField(upload_to='images/logo/%Y/%m/%d/',max_length=2000,blank=True ,null =True)

    call_no =  models.CharField(max_length=200, default='020 2020 405', blank=True,null=True)
    info_mail = models.EmailField(default='info@uda-party.com')
    office_location = models.CharField(max_length=200,default="Hustler Center | Nairobi Kenya", blank=True,null=True)
    designer = models.CharField(max_length=200, default='+254712748566', blank=True,null=True)
    designer_link = models.URLField(default="https://www.linkedin.com/in/kipngeno-gibeon-27b9765a/")

    instagram_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
        
        FieldPanel('logofooter'),

        FieldPanel('office_location'),
        FieldPanel('info_mail'),
        FieldPanel('call_no'),
        FieldPanel('designer'),
        FieldPanel('designer_link'),

        FieldPanel('instagram_link'),
        FieldPanel('twitter_link'),
        FieldPanel('youtube_link'),
        FieldPanel('facebook_link'),
    ]

    def __str__(self):
        return str(self.text)
        
        
        
        
        
        
class InfoPage(Page):
    
    # image0 = models.ImageField(upload_to='images/intro/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    # signature_01 = models.ImageField(upload_to='images/signature/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    intro_quote1 = models.CharField(max_length=200, blank=True,null=True)
    intro_quote2 = models.CharField(max_length=200, blank=True,null=True)
    intro_quote3 = models.CharField(max_length=200, blank=True,null=True)

    body = RichTextField(blank=True)
#     latest_new_title = models.CharField(max_length=200, default='Latest News', blank=True,null=True)
    
    tittle1 = models.CharField(max_length=250 ,blank=True,null=True)  
    tittle2 = models.CharField(max_length=250 ,blank=True,null=True)
    tittle3 = models.CharField(max_length=250 ,blank=True,null=True) 
    tittle4 = models.CharField(max_length=250 ,blank=True,null=True)

    bodi1 = models.CharField(max_length=250 ,blank=True,null=True) 
    bodi2 = models.CharField(max_length=250 ,blank=True,null=True)
    bodi3 = models.CharField(max_length=250 ,blank=True,null=True)
    bodi4 = models.CharField(max_length=250 ,blank=True,null=True)


    advert = models.ForeignKey(
        'home.Advert',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')
# 
    header = models.ForeignKey(
        'home.Header',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')

    footer = models.ForeignKey(
        'home.Footer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')        


    content_panels=Page.content_panels + [
        SnippetChooserPanel('advert'),
        SnippetChooserPanel('header'),
        SnippetChooserPanel('footer'),
        FieldPanel('body',classname = "full"),
        # FieldPanel('image0'),
        # FieldPanel('signature_01'),      


        FieldPanel('intro_quote1'),
        FieldPanel('intro_quote2'),
        FieldPanel('intro_quote3'),

        FieldPanel('tittle1'),
        FieldPanel('bodi1'),
        FieldPanel('tittle2'),
        FieldPanel('bodi2'),
        FieldPanel('tittle3'),
        FieldPanel('bodi3'),
        FieldPanel('tittle4'),
        FieldPanel('bodi4'),

#         # InlinePanel('latestnewz',label="Latest News"),


    ]

    
class FaqPage(Page):
    
    # image0 = models.ImageField(upload_to='images/intro/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    # signature_01 = models.ImageField(upload_to='images/signature/%Y/%m/%d/',max_length=2000,blank=True ,null =True)
    intro_quote1 = models.CharField(max_length=200, blank=True,null=True)
    intro_quote2 = models.CharField(max_length=200, blank=True,null=True)
    intro_quote3 = models.CharField(max_length=200, blank=True,null=True)

    body = RichTextField(blank=True)
#     latest_new_title = models.CharField(max_length=200, default='Latest News', blank=True,null=True)
    
    tittle1 = models.CharField(max_length=250 ,blank=True,null=True)  
    tittle2 = models.CharField(max_length=250 ,blank=True,null=True)
    tittle3 = models.CharField(max_length=250 ,blank=True,null=True) 
    tittle4 = models.CharField(max_length=250 ,blank=True,null=True)

    bodi1 = models.CharField(max_length=250 ,blank=True,null=True) 
    bodi2 = models.CharField(max_length=250 ,blank=True,null=True)
    bodi3 = models.CharField(max_length=250 ,blank=True,null=True)
    bodi4 = models.CharField(max_length=250 ,blank=True,null=True)


    advert = models.ForeignKey(
        'home.Advert',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')
# 
    header = models.ForeignKey(
        'home.Header',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')

    footer = models.ForeignKey(
        'home.Footer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,related_name='+')        


    content_panels=Page.content_panels + [
        SnippetChooserPanel('advert'),
        SnippetChooserPanel('header'),
        SnippetChooserPanel('footer'),
        FieldPanel('body',classname = "full"),
        # FieldPanel('image0'),
        # FieldPanel('signature_01'),      


        FieldPanel('intro_quote1'),
        FieldPanel('intro_quote2'),
        FieldPanel('intro_quote3'),

        FieldPanel('tittle1'),
        FieldPanel('bodi1'),
        FieldPanel('tittle2'),
        FieldPanel('bodi2'),
        FieldPanel('tittle3'),
        FieldPanel('bodi3'),
        FieldPanel('tittle4'),
        FieldPanel('bodi4'),

#         # InlinePanel('latestnewz',label="Latest News"),


    ]





        




        
