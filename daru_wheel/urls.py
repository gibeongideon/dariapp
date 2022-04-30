from . import temp_views as views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_view

router = DefaultRouter()
router.register(r"stake", api_view.StakeViewSet, basename="Stake")

app_name = "daru_wheel"

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.spin, name="spin"),
    path("r/<str:refer_code>/", views.spin, name="spin"),
    path("spinx", views.spinx, name="spinx"),    
    path("stakes", views.stakes, name="stakes"),
]
