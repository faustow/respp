from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import TRAINING_COLUMNS
from properties.models import Property
from properties.serializers import PropertySerializer


class PropertiesAPIView(APIView):
    """
    Endpoint para listar y crear propiedades.
    """

    def get(self, request, *args, **kwargs):
        """
        Listar propiedades existentes.
        """
        properties = Property.objects.all()
        data = properties.values(*TRAINING_COLUMNS)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Add data_source=2 and dataset="training" to the request data
        request.data["data_source"] = 2
        request.data["dataset"] = "training"
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            property_instance = serializer.save()  # Guarda la propiedad
            return Response(
                {"message": f"Property '{property_instance.id}' created"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
