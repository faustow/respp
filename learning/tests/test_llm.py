from django.test import TestCase

from learning.llm import (
    generate_property_features,
    generate_prompt_for_sales_listing,
    generate_sales_listing,
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
        }
        self.empty_property_data = {}

    def test_generate_property_features(self):
        features = generate_property_features(self.property_data)
        self.assertIsInstance(features, list)
        self.assertIn("Lot size: 12000 sq ft.", features)
        self.assertIn("Living area: 2500 sq ft.", features)
        self.assertIn("Garage: space for 2 cars.", features)
        self.assertNotIn("Overall quality rating", generate_property_features(self.empty_property_data))

    def test_generate_prompt_for_sales_listing(self):
        prompt = generate_prompt_for_sales_listing(self.description, self.property_data)
        self.assertIn("Beautiful family home with modern features.", prompt)
        self.assertIn("Lot size: 12000 sq ft.", prompt)
        self.assertIn("Living area: 2500 sq ft.", prompt)
        self.assertIn("Year built: 2015.", prompt)
        self.assertIn("Garage: space for 2 cars.", prompt)
        self.assertIn("Neighborhood: OldTown.", prompt)
        self.assertIn("Style: Colonial.", prompt)

    def test_generate_sales_listing(self):
        result = generate_sales_listing(self.description, self.property_data)
        print("-" * 80)
        print(f"Generated text: {result}")
        print("." * 80)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")  # Ensure the generated text is not empty.
        self.assertIn("family home", result)
        self.assertIn("12000 sq ft", result)

    def test_generate_customer_profiles_with_prompt(self):
        listing_text = (
            "This is a charming three-bedroom home with a spacious backyard, perfect for families. "
            "Located in the heart of the OldTown neighborhood, this property includes a modern kitchen, "
            "two full bathrooms, and a garage for two cars."
        )
        result = generate_customer_profiles(listing_text)
        print("<>" * 80)
        print(f"Generated customer profiles: {result}")
        print("," * 80)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")  # Ensure the generated text is not empty.
        self.assertIn("Occupation", result)
        self.assertIn("Annual income range", result)
        self.assertIn("Key reasons", result)
        self.assertIn("Lifestyle or demographic information", result)

    def test_generate_customer_profiles_empty_input(self):
        empty_result = generate_customer_profiles("")
        self.assertIsInstance(empty_result, str)
        self.assertEqual(empty_result, "No customer profiles")
