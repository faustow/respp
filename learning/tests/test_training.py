from math import sqrt

import joblib
import torch
from django.test import TestCase
from sklearn.metrics import mean_squared_error, r2_score

from learning.models import AmesNet
from learning.training import prepare_dataset

BASELINE_RMSE = 39130.782971977445
BASELINE_R2 = 0.7233098745346069


class AmesNetRegressionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Cargar los datos de prueba del conjunto "test"
        X_test, y_test = prepare_dataset("test")
        cls.labels = torch.tensor(y_test, dtype=torch.float32)

        # Cargar el escalador y escalar los datos de prueba
        scaler = joblib.load("scaler.pkl")
        X_test_scaled = scaler.transform(X_test)
        cls.data = torch.tensor(X_test_scaled, dtype=torch.float32)

        # Inicializar el modelo
        cls.model = AmesNet(input_dim=7)
        cls.model.load_state_dict(torch.load("ames_model.pth", map_location=torch.device("cpu"), weights_only=True))
        cls.model.eval()

    def test_r2_score(self):
        with torch.no_grad():
            predictions = self.model(self.data).squeeze().numpy()
        r2 = r2_score(self.labels.numpy(), predictions)
        print(f"R^2 score: {r2}")
        self.assertGreaterEqual(r2, BASELINE_R2, f"R^2 score too low: {r2}")

    def test_rmse(self):
        with torch.no_grad():
            predictions = self.model(self.data).squeeze().numpy()
        mse = mean_squared_error(self.labels.numpy(), predictions)
        rmse = sqrt(mse)
        print(f"RMSE: {rmse}")
        self.assertLessEqual(rmse, BASELINE_RMSE, f"MSE too high: {rmse}")
