from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

from .views import user_detail, access_token_detail


urlpatterns = [
    url(r"^$", RedirectView.as_view(pattern_name="account_login", permanent=False), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^tokeninfo/$", access_token_detail, name="access_token"),
    url(r"^me/$", user_detail, name="user_detail"),
    url(r"^oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
