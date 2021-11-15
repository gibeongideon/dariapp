from django.urls import path, re_path
from home import views
from daru_wheel.temp_views import spin

# from daruwheel import views as spinview

app_name = "home"

urlpatterns = [
    # Matches any html file    
    # The home pages
    path("", views.homepage, name="homepage"),
    path("<str:refer_code>/", views.homepage, name="homepage"),
    # path('', views.index, name='index'),
    path("wallet", views.deposit_withraw, name="deposit_withraw"),
    path("affiliate", views.affiliate, name="affiliate"),
    # path("", views.subscribe, name="subscribe"),
    # path("support", views.support, name="support"),
    # re_path(r"^.*\/", views.pages, name="pages"),
]
