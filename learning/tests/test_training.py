import os

import torch
from django.test import TestCase
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from learning.models import AmesNet
from learning.training import fetch_data

BASELINE_MSE = 1289987200
BASELINE_R2 = 0.8417234420776367


class AmesNetRegressionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up a fixed dataset and model for all tests.
        """
        super().setUpClass()
        cls.data, cls.labels = fetch_data()
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
            cls.data, cls.labels, test_size=0.2, random_state=42
        )

        # Initialize the model and load weights
        cls.model = AmesNet(input_dim=cls.data.shape[1])
        model_path = "ames_model.pth"
        if os.path.exists(model_path):
            cls.model.load_state_dict(torch.load(model_path))
        else:
            raise FileNotFoundError(f"Trained model weights not found at {model_path}")
        cls.model.eval()

    def test_r2_score(self):
        """
        Ensure the R^2 score meets a minimum threshold.
        """
        with torch.no_grad():
            predictions = self.model(torch.tensor(self.X_test, dtype=torch.float32)).squeeze().numpy()
        r2 = r2_score(self.y_test, predictions)
        print(f"R^2 score: {r2}")
        self.assertGreaterEqual(
            r2,
            BASELINE_R2,
            f"R^2 score is too low: {r2}. Model might have regressed.",
        )

    def test_mse(self):
        """
        Ensure the Mean Squared Error (MSE) meets a maximum threshold.
        """
        with torch.no_grad():
            predictions = self.model(torch.tensor(self.X_test, dtype=torch.float32)).squeeze().numpy()
        mse = mean_squared_error(self.y_test, predictions)
        print(f"MSE: {mse}")
        self.assertLessEqual(
            mse,
            BASELINE_MSE,
            f"MSE is too high: {mse}. Model might have regressed.",
        )
