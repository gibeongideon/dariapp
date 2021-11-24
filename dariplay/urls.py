from .views import MatchRecordView,MatchViewSet,MatchView
from rest_framework.routers import DefaultRouter

from django.urls import path, include



router = DefaultRouter()

router.register(r'match', MatchViewSet)

app_name = "dariplay"

urlpatterns = [
   path('', include(router.urls)),
   path("api/", MatchRecordView.as_view(), name="matches"),
   path('files/<int:pk>/', MatchView.as_view()),# Main
]
