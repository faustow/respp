import torch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.apps import scaler, model
from learning.serializers import PredictPriceSerializer


class PredictPriceAPIView(APIView):
    """
    API endpoint para predecir el precio de venta.
    """

    def post(self, request, *args, **kwargs):
        serializer = PredictPriceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # Extraer características en el orden esperado
        input_features = [
            validated_data["lotarea"],
            validated_data["overallqual"],
            validated_data["overallcond"],
            int(validated_data["centralair"]),
            validated_data["fullbath"],
            validated_data["bedroomabvgr"],
            validated_data["garagecars"],
        ]
        # Preprocesar y escalar los datos
        scaled_features = scaler.transform([input_features])
        with torch.no_grad():
            prediction = model(torch.tensor(scaled_features, dtype=torch.float32)).item()

        return Response({"predicted_price": round(prediction, 2)}, status=status.HTTP_200_OK)
