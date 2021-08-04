from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
admin.site.site_header = "DariApp Admin"


urlpatterns = [
    path(
        settings.SECRET_ADMIN_URL + "/dj-admin/",
        admin.site.urls),
    path(
        settings.SECRET_ADMIN_URL + "/admin/",
        include(wagtailadmin_urls)),

    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path("", include("home.urls", namespace="dashboard")),
    path("user/", include("users.urls", namespace="users")),
    path("daru_wheel/", include("daru_wheel.urls", namespace="daru_wheel")),
    path("account/", include("account.urls", namespace="account")),
    path("pesa/", include("mpesa_api.core.urls", "mpesa")),
    path('paypal/', include('paypal.standard.ipn.urls')), 

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
