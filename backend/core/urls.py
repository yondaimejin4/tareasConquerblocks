from django.urls import path

from .views import (
    ContactLeadCreateAPIView,
    FeaturedServiceListAPIView,
    HomePageView,
    ServiceListAPIView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("api/services/", ServiceListAPIView.as_view(), name="service-list-api"),
    path(
        "api/services/featured/",
        FeaturedServiceListAPIView.as_view(),
        name="service-featured-api",
    ),
    path("api/contact/", ContactLeadCreateAPIView.as_view(), name="contact-create-api"),
]
