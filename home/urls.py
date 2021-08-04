from django.urls import path, re_path
from home import views
from daru_wheel.temp_views import spin

# from daruwheel import views as spinview

app_name = "home"

urlpatterns = [
    # Matches any html file
    
    # The home page
    path("", views.homepage, name="homepage"),
    # path('', views.index, name='index'),
    path("deposit_withraw", views.deposit_withraw, name="deposit_withraw"),
    path("affiliate", views.affiliate, name="affiliate"),
    # path("maps", views.maps, name="maps"),
    # path("topo", views.topo, name="topo"),
    # path("support", views.support, name="support"),
    # re_path(r"^.*\/", views.pages, name="pages"),
]
