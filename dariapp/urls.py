from django.conf import settings
from django.urls import include, path
from django.contrib import admin

admin.site.site_header = "Darius Option"


urlpatterns = [
    path(
    settings.SECRET_ADMIN_URL + "/admin/",admin.site.urls),    
    path("", include("daru_wheel.urls", namespace="daru_wheel")),
    path("user/", include("users.urls", namespace="users")),
    path("account/", include("account.urls", namespace="account")),
    path("pesa/", include("mpesa_api.core.urls", "mpesa")),
    path('paypal/', include('paypal.standard.ipn.urls')), 

]


from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
