from django.urls import path, include, re_path

v1_patterns = [
    path("auth/", include("api_authservices.urls")),
    path("users/", include("api_users.urls")),
    path("department/", include(("api_departments.urls"))),
    path("office/", include(("api_offices.urls"))),
    path("field/", include(("api_fields.urls"))),
    path("news/", include(("api_news.urls"))),
    path("service/", include(("api_services.urls"))),
    path("evaluate/", include(("api_evaluates.urls"))),
    path("statistics/", include(("api_statistic.urls"))),
    path("", include(("api_files.urls"))),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = [
    path("", include(v1_patterns)),
]
