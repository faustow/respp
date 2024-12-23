import os
import numpy as np
import torch
from django.test import TestCase
from sklearn.metrics import mean_squared_error, r2_score

from learning.models import AmesNet

BASELINE_MSE = 1888914432.0
BASELINE_R2 = 0.7682373523712158



class AmesNetRegressionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the dataset and load the trained model for all tests.
        """
        super().setUpClass()
        torch.manual_seed(42)
        np.random.seed(42)

        # Load test data
        cls.data = np.load("data_test.npy")
        cls.labels = np.load("labels_test.npy")

        # Initialize the model
        cls.model = AmesNet(input_dim=cls.data.shape[1])
        model_path = "ames_model.pth"
        if os.path.exists(model_path):
            cls.model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
        else:
            raise FileNotFoundError(f"Trained model weights not found at {model_path}")
        cls.model.eval()

    def test_r2_score(self):
        """
        Ensure the R^2 score meets a minimum threshold using pre-trained weights.
        """
        with torch.no_grad():
            predictions = self.model(torch.tensor(self.data, dtype=torch.float32)).squeeze().numpy()
        r2 = r2_score(self.labels, predictions)
        print(f"R^2 score: {r2}")
        self.assertGreaterEqual(
            r2,
            BASELINE_R2,
            f"R^2 score is too low: {r2}. Model might have regressed.",
        )

    def test_mse(self):
        """
        Ensure the Mean Squared Error (MSE) meets a maximum threshold using pre-trained weights.
        """
        with torch.no_grad():
            predictions = self.model(torch.tensor(self.data, dtype=torch.float32)).squeeze().numpy()
        mse = mean_squared_error(self.labels, predictions)
        print(f"MSE: {mse}")
        self.assertLessEqual(
            mse,
            BASELINE_MSE,
            f"MSE is too high: {mse}. Model might have regressed.",
        )