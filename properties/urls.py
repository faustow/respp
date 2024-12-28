from django.urls import path

from properties.views import PropertiesAPIView, ListingAPIView

urlpatterns = [
    path("", PropertiesAPIView.as_view(), name="properties"),
    path("listings/", ListingAPIView.as_view(), name="listings"),
    path("listings/<int:listing_id>/", ListingAPIView.as_view(), name="property-listings"),
]
