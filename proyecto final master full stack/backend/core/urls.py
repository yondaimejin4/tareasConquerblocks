from django.urls import path, re_path

from .spa_views import ReactAssetView, ReactFaviconView, ReactSpaView
from .views import (
    ContactLeadCreateAPIView,
    CsrfCookieAPIView,
    FeaturedServiceListAPIView,
    HealthAPIView,
    HomePageView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    MyContributionCreateAPIView,
    MyProjectRequestDetailAPIView,
    MyProjectRequestListCreateAPIView,
    RegisterAPIView,
    ServiceListAPIView,
)

urlpatterns = [
    path("django/", HomePageView.as_view(), name="home-django"),
    path("api/health/", HealthAPIView.as_view(), name="api-health"),
    path("api/services/", ServiceListAPIView.as_view(), name="service-list-api"),
    path(
        "api/services/featured/",
        FeaturedServiceListAPIView.as_view(),
        name="service-featured-api",
    ),
    path("api/contact/", ContactLeadCreateAPIView.as_view(), name="contact-create-api"),
    path("api/auth/csrf/", CsrfCookieAPIView.as_view(), name="auth-csrf"),
    path("api/auth/register/", RegisterAPIView.as_view(), name="auth-register"),
    path("api/auth/login/", LoginAPIView.as_view(), name="auth-login"),
    path("api/auth/logout/", LogoutAPIView.as_view(), name="auth-logout"),
    path("api/auth/me/", MeAPIView.as_view(), name="auth-me"),
    path(
        "api/my-requests/",
        MyProjectRequestListCreateAPIView.as_view(),
        name="my-requests-list",
    ),
    path(
        "api/my-requests/<int:pk>/",
        MyProjectRequestDetailAPIView.as_view(),
        name="my-requests-detail",
    ),
    path(
        "api/my-requests/<int:pk>/contributions/",
        MyContributionCreateAPIView.as_view(),
        name="my-requests-contribution",
    ),
    path("assets/<path:filepath>", ReactAssetView.as_view(), name="react-asset"),
    path("favicon.svg", ReactFaviconView.as_view(), name="react-favicon"),
    re_path(r"^.*$", ReactSpaView.as_view(), name="react-spa"),
]
