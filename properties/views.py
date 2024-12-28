from django.db.models import F
from django.db.models.functions import Abs
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import TRAINING_COLUMNS
from properties.models import Property, Listing
from properties.serializers import PropertySerializer, ListingSerializer


class PropertiesAPIView(APIView):
    """
    Endpoint para listar y crear propiedades.
    """

    def get(self, request, *args, **kwargs):
        """
        Listar propiedades existentes o buscar la propiedad más cercana a los parámetros dados.
        """
        query_params = request.query_params

        if query_params:
            try:
                # Obtener valores de los parámetros de consulta
                lotarea = int(query_params.get("lotarea", 0))
                overallqual = int(query_params.get("overallqual", 0))
                overallcond = int(query_params.get("overallcond", 0))
                centralair = 1 if query_params.get("centralair", "Yes") == "Yes" else 0
                fullbath = int(query_params.get("fullbath", 0))
                bedroomabvgr = int(query_params.get("bedroomabvgr", 0))
                garagecars = int(query_params.get("garagecars", 0))

                # Calcular la métrica de distancia
                properties = Property.objects.annotate(
                    distance=(
                            Abs(F("lotarea") - lotarea) +
                            Abs(F("overallqual") - overallqual) +
                            Abs(F("overallcond") - overallcond) +
                            Abs(F("centralair") - centralair) +
                            Abs(F("fullbath") - fullbath) +
                            Abs(F("bedroomabvgr") - bedroomabvgr) +
                            Abs(F("garagecars") - garagecars)
                    )
                ).order_by("distance", "-yrsold", "-mosold")

                closest_property = properties.first()
                if closest_property:
                    serializer = PropertySerializer(closest_property)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(
                    {"message": "No matching property found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            except ValueError as e:
                return Response(
                    {"error": f"Invalid query parameters: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Si no hay parámetros de consulta, devolver todas las propiedades
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


class ListingAPIView(APIView):
    def post(self, request):
        """
        Crear un nuevo listing asociado a una propiedad.
        """
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, property_id):
        """
        Obtener todos los listings asociados a una propiedad.
        """
        listings = Listing.objects.filter(property_id=property_id)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
