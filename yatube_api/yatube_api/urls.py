from api.urls import v1_router
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/v1/", include(v1_router.urls)),
    path("redoc/", TemplateView.as_view(template_name="redoc.html"),
         name="redoc"),
    path("api/v1/", include("djoser.urls")),
    # JWT-эндпоинты, для управления JWT-токенами:
    path("api/v1/", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
