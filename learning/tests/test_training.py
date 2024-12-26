import joblib
import torch
from django.test import TestCase
from sklearn.metrics import mean_squared_error, r2_score

from learning.models import AmesNet
from properties.models import Property

BASELINE_MSE = 1531218048.0
BASELINE_R2 = 0.7233098745346069


class AmesNetRegressionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Fetch test data from the database
        test_data = Property.objects.filter(dataset="test")
        cls.data = torch.tensor(test_data.values_list(
            "lotarea", "overallqual", "overallcond", "centralair", "fullbath",
            "bedroomabvgr", "garagecars"
        ), dtype=torch.float32)
        cls.labels = torch.tensor(test_data.values_list("saleprice", flat=True), dtype=torch.float32)

        # Cargar el escalador y escalar los datos de prueba
        scaler = joblib.load("scaler.pkl")
        cls.data = torch.tensor(scaler.transform(cls.data.numpy()), dtype=torch.float32)

        # Initialize the model
        cls.model = AmesNet(input_dim=7)
        cls.model.load_state_dict(torch.load("ames_model.pth", map_location=torch.device("cpu")))
        cls.model.eval()

    def test_r2_score(self):
        with torch.no_grad():
            predictions = self.model(self.data).squeeze().numpy()
        r2 = r2_score(self.labels.numpy(), predictions)
        print(f"R^2 score: {r2}")
        self.assertGreaterEqual(r2, BASELINE_R2, f"R^2 score too low: {r2}")

    def test_mse(self):
        with torch.no_grad():
            predictions = self.model(self.data).squeeze().numpy()
        mse = mean_squared_error(self.labels.numpy(), predictions)
        print(f"MSE: {mse}")
        self.assertLessEqual(mse, BASELINE_MSE, f"MSE too high: {mse}")
