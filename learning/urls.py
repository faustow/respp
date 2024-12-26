from django.urls import path

from .views import PredictPriceAPIView

urlpatterns = [
    path("predict-price/", PredictPriceAPIView.as_view(), name="predict-price"),
]
