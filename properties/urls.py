from django.urls import path
from properties.views import PropertiesAPIView

urlpatterns = [
    path("", PropertiesAPIView.as_view(), name="properties"),
]