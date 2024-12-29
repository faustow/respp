from django.test import TestCase

from learning.llm import (
    generate_property_features,
    generate_prompt_for_sales_listing,
    generate_sales_listing,
    generate_customer_profiles_prompt,
    generate_customer_profiles,
)


class TestLLMFunctions(TestCase):
    def setUp(self):
        self.description = "Beautiful family home with modern features."
        self.property_data = {
            "lotarea": 12000,
            "grlivarea": 2500,
            "yearbuilt": 2015,
            "overallqual": 9,
            "fullbath": 2,
            "garagecars": 2,
            "neighborhood": "OldTown",
            "housestyle": "Colonial",
            "saleprice": 350000,
        }
        self.empty_property_data = {}

    def test_generate_property_features_valid_data(self):
        features = generate_property_features(self.property_data)
        self.assertIsInstance(features, list)
        self.assertIn("Lot size: 12000 sq ft.", features)
        self.assertIn("Living area: 2500 sq ft.", features)
        self.assertIn("Year built: 2015.", features)
        self.assertIn("Garage: space for 2 cars.", features)

    def test_generate_property_features_empty_data(self):
        features = generate_property_features(self.empty_property_data)
        self.assertIsInstance(features, list)
        self.assertEqual(features, [])

    def test_generate_prompt_for_sales_listing(self):
        prompt = generate_prompt_for_sales_listing(self.description, self.property_data)
        self.assertIsInstance(prompt, str)
        self.assertIn("Beautiful family home with modern features.", prompt)
        self.assertIn("Lot size: 12000 sq ft.", prompt)
        self.assertIn("Living area: 2500 sq ft.", prompt)
        self.assertIn("Avoid repeating features.", prompt)

    def test_generate_sales_listing(self):
        result = generate_sales_listing(self.description, self.property_data)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")  # Ensure the generated text is not empty.
        self.assertIn("$", result)
        self.assertIn("350", result)

    def test_generate_customer_profiles_prompt(self):
        prompt = generate_customer_profiles_prompt(self.description, self.property_data)
        self.assertIsInstance(prompt, str)
        self.assertIn("Task: List", prompt)
        self.assertIn(f"Highlights: {self.description}", prompt)
        self.assertIn("Make each occupation unique", prompt)

    def test_generate_customer_profiles(self):
        result = generate_customer_profiles(self.description, self.property_data)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")  # Ensure the generated text is not empty.

    def test_generate_customer_profiles_empty_data(self):
        result = generate_customer_profiles("", self.empty_property_data)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "No info given, impossible to create customer profiles")
