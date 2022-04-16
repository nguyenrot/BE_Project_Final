"""Project_Final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

shema_view = get_schema_view(
    openapi.Info(
        title="Project Final",
        default_version="v1",
        description="APIs for Project Final",
        contact=openapi.Contact(email="phamkynguyen753@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    # url('admin/', admin.site.urls),
    path("api/", include(("api_base.urls"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^(?P<format>\.json|\.yaml)$', shema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'', shema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'', shema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
