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
