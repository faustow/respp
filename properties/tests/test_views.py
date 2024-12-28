from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from properties.models import Property


class PropertiesAPITestCase(TestCase):
    def setUp(self):
        Property.objects.all().delete()
        self.client = APIClient()
        self.url = "/api/properties/"

    def test_list_properties(self):
        amount = Property.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), amount)

    def test_create_property_success(self):
        amount = Property.objects.count()
        valid_data = {
            "lotarea": 10000,
            "overallqual": 7,
            "overallcond": 5,
            "centralair": 1,
            "fullbath": 2,
            "bedroomabvgr": 3,
            "garagecars": 2,
            "saleprice": 250000,
        }
        response = self.client.post(self.url, valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), amount + 1)
        self.assertEqual(Property.objects.last().saleprice, valid_data["saleprice"])

    def test_create_property_adds_default_fields(self):
        valid_data = {
            "lotarea": 20000,
            "overallqual": 8,
            "overallcond": 5,
            "centralair": 1,
            "fullbath": 2,
            "bedroomabvgr": 3,
            "garagecars": 2,
            "saleprice": 350000,
        }
        response = self.client.post(self.url, valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        last_property = Property.objects.last()
        self.assertEqual(last_property.dataset, 'training')
        self.assertEqual(last_property.data_source, 2)

    def test_create_property_failure(self):
        invalid_data = {
            "lotarea": -5000,  # Invalid value
            "overallqual": 15,  # Invalid value
        }
        amount = Property.objects.count()
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Property.objects.count(), amount)  # No new property should be created


class PropertiesAPISearchTestCase(TestCase):
    def setUp(self):
        Property.objects.all().delete()
        self.url = "/api/properties/"
        # Crear propiedades de prueba
        Property.objects.create(
            lotarea=10000, overallqual=7, overallcond=5, centralair=1,
            fullbath=2, bedroomabvgr=3, garagecars=2,
            yrsold=2022, mosold=6, saleprice=250000
        )
        Property.objects.create(
            lotarea=9500, overallqual=6, overallcond=5, centralair=1,
            fullbath=2, bedroomabvgr=3, garagecars=2,
            yrsold=2023, mosold=5, saleprice=240000
        )
        Property.objects.create(
            lotarea=10000, overallqual=7, overallcond=5, centralair=1,
            fullbath=2, bedroomabvgr=3, garagecars=2,
            yrsold=2023, mosold=7, saleprice=260000
        )

    def test_search_closest_property(self):
        query_params = {
            "lotarea": 10000,
            "overallqual": 7,
            "overallcond": 5,
            "centralair": "Yes",
            "fullbath": 2,
            "bedroomabvgr": 3,
            "garagecars": 2,
        }
        response = self.client.get(self.url, query_params)

        # Verificar que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)

        # Verificar que la propiedad más reciente sea devuelta
        data = response.json()
        self.assertEqual(data["yrsold"], 2023)
        self.assertEqual(data["mosold"], 7)
