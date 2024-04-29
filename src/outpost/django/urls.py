"""
Outpost URL Configuration
"""
import logging
from importlib import import_module

import django
from django.apps import apps
from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve
from rest_framework.authtoken import views as authtoken

logger = logging.getLogger(__name__)

js_info_dict = {
    "packages": ("recurrence",),
}

urlpatterns = []

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.extend(
        [
            url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
            url(
                r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
            ),
        ]
    )
    urlpatterns.extend([url(r"^__debug__/", include(debug_toolbar.urls))])

if not settings.DEBUG:
    admin.site.login = login_required(admin.site.login)

urlpatterns.extend(
    [
        url(r"^admin/", admin.site.urls),
        url(r"^jsi18n/$", JavaScriptCatalog.as_view(), js_info_dict),
        url(r"^auth/api/", include("rest_framework.urls", namespace="rest_framework")),
        url(r"^prometheus/", include("django_prometheus.urls")),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        url(r"^auth/token/", authtoken.obtain_auth_token),
        url(
            r"^saml2/",
            include(
                ("djangosaml2.urls", "saml2")
                if django.VERSION >= (2, 1)
                else "djangosaml2.urls",
                namespace="saml2",
            ),
        ),
    ]
)

for app in sorted(apps.get_app_configs(), key=lambda app: app.label):
    if not app.name.startswith("outpost.django."):
        continue
    logger.debug(f"Importing urls from {app.name}")
    urls = f"{app.name}.urls"
    try:
        module = import_module(urls)
    except ModuleNotFoundError:
        continue
    path = getattr(module, "BASE_PATH", f"^{app.label}/")
    urlpatterns.append(url(path, include(urls, namespace=app.label)))

urlpatterns.extend(
    [
        url(
            r"^",
            include(("django.contrib.auth.urls", "accounts"), namespace="accounts"),
        ),
    ]
)
