from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin


urlpatterns = [
    url(r"^$", RedirectView.as_view(pattern_name="account_login", permanent=False), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"", include("pinax.identity.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
