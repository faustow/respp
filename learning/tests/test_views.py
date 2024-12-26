from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from learning.serializers import PredictPriceSerializer


class PredictPriceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/learning/predict-price/"
        self.valid_payload = {
            "lotarea": 8450,
            "overallqual": 7,
            "overallcond": 5,
            "centralair": True,
            "fullbath": 2,
            "bedroomabvgr": 3,
            "garagecars": 2,
        }

    def test_valid_request(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("predicted_price", response.data)
        self.assertIsInstance(response.data["predicted_price"], float)

    def test_missing_fields(self):
        payload = self.valid_payload.copy()
        payload.pop("lotarea")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("lotarea", response.data)

    def test_invalid_field_types(self):
        payload = self.valid_payload.copy()
        payload["lotarea"] = "invalid"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("lotarea", response.data)

    def test_empty_payload(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("lotarea", response.data)

    def test_serializer_validation(self):
        """
        Test directo al serializer para validar su funcionamiento.
        """
        serializer = PredictPriceSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())

        invalid_payload = self.valid_payload.copy()
        invalid_payload["lotarea"] = "invalid"
        serializer = PredictPriceSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())