from math import sqrt

import joblib
import pandas as pd
import torch
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset

from config.settings import AMES_MODEL_FILENAME, SCALER_FILENAME
from learning.models import AmesNet
from properties.models import Property


class AmesDataset(Dataset):
    def __init__(self, features, labels):
        self.data = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


def train_and_evaluate():
    # Cargar datos de la base de datos
    training_data = Property.objects.filter(dataset="training").values_list(
        "lotarea", "overallqual", "overallcond", "centralair", "fullbath", "bedroomabvgr", "garagecars", "saleprice"
    )
    validation_data = Property.objects.filter(dataset="validation").values_list(
        "lotarea", "overallqual", "overallcond", "centralair", "fullbath", "bedroomabvgr", "garagecars", "saleprice"
    )

    # Convertir a DataFrames para escalado
    training_df = pd.DataFrame(training_data,
                               columns=["lotarea", "overallqual", "overallcond", "centralair", "fullbath",
                                        "bedroomabvgr", "garagecars", "saleprice"])
    validation_df = pd.DataFrame(validation_data,
                                 columns=["lotarea", "overallqual", "overallcond", "centralair", "fullbath",
                                          "bedroomabvgr", "garagecars", "saleprice"])

    # Separar características y etiquetas
    X_train = training_df.drop(columns=["saleprice"]).values
    y_train = training_df["saleprice"].values
    X_val = validation_df.drop(columns=["saleprice"]).values
    y_val = validation_df["saleprice"].values

    # Ajustar el escalador con el conjunto de entrenamiento
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    # Crear datasets y dataloaders
    train_dataset = AmesDataset(X_train_scaled, y_train)
    val_dataset = AmesDataset(X_val_scaled, y_val)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)

    # Inicializar modelo, pérdida y optimizador
    model = AmesNet(input_dim=X_train_scaled.shape[1])
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Entrenamiento
    epochs = 50
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch_data, batch_labels in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_data).squeeze()
            loss = criterion(predictions, batch_labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader):.4f}")

    # Guardar el escalador
    joblib.dump(scaler, SCALER_FILENAME)
    print(f"Scaler saved to {SCALER_FILENAME}.")

    # Guardar modelo
    torch.save(model.state_dict(), AMES_MODEL_FILENAME)
    print(f"Model saved to {AMES_MODEL_FILENAME}.")

    # Validación
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch_data, batch_labels in val_loader:
            preds = model(batch_data).squeeze()
            predictions.extend(preds.numpy())
            true_labels.extend(batch_labels.numpy())

    # Métricas de evaluación
    mse = mean_squared_error(true_labels, predictions)
    rmse = sqrt(mse)
    r2 = r2_score(true_labels, predictions)

    print(f"Validation Loss (RMSE): {rmse:.4f}")
    print(f"R^2 Score: {r2:.4f}")
    return rmse, r2


def load_model_and_scaler():
    """
    Carga el modelo de AmesNet y el escalador.
    """
    model = AmesNet(input_dim=7)
    model.load_state_dict(torch.load(AMES_MODEL_FILENAME, map_location=torch.device("cpu")))
    model.eval()
    scaler = joblib.load(SCALER_FILENAME)
    return model, scaler
