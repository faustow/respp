from math import sqrt

import joblib
import pandas as pd
import torch
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader

from config.settings import AMES_MODEL_FILENAME, SCALER_FILENAME, BATCH_SIZE, TRAINING_COLUMNS
from learning.models import AmesNet, AmesDataset
from properties.models import Property


def prepare_dataset(dataset_name):
    """
    Carga y limpia los datos desde la base de datos según el nombre del dataset.
    """
    data = Property.objects.filter(dataset=dataset_name).values_list(*TRAINING_COLUMNS)

    # Convertir a DataFrame
    df = pd.DataFrame(data, columns=TRAINING_COLUMNS)

    # Reemplazar valores nulos
    df.fillna(0, inplace=True)  # Sustituye None con 0 o ajusta según las necesidades

    # Separar características y etiquetas
    X = df.drop(columns=["saleprice"]).values
    y = df["saleprice"].values

    return X, y


def scale_data(X_train, X_val):
    """
    Escala los datos de entrenamiento y validación utilizando StandardScaler.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    save_scaler(scaler, SCALER_FILENAME)
    return X_train_scaled, X_val_scaled


def create_dataloader(features, labels, batch_size, shuffle=True):
    """
    Crea un DataLoader a partir de características y etiquetas.
    """
    dataset = AmesDataset(features, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def initialize_model(input_dim):
    """
    Inicializa el modelo AmesNet.
    """
    return AmesNet(input_dim=input_dim)


def train_model(model, train_loader, criterion, optimizer, epochs):
    """
    Entrena el modelo utilizando un DataLoader.
    """
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


def save_scaler(scaler, filename):
    """
    Guarda el escalador en un archivo.
    """
    joblib.dump(scaler, filename)
    print(f"Scaler saved to {filename}.")


def save_model(model, filename):
    """
    Guarda el modelo entrenado en un archivo.
    """
    torch.save(model.state_dict(), filename)
    print(f"Model saved to {filename}.")


def validate_model(model, val_loader):
    """
    Evalúa el modelo utilizando el conjunto de validación.
    """
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch_data, batch_labels in val_loader:
            preds = model(batch_data).squeeze()
            predictions.extend(preds.numpy())
            true_labels.extend(batch_labels.numpy())

    mse = mean_squared_error(true_labels, predictions)
    rmse = sqrt(mse)
    r2 = r2_score(true_labels, predictions)
    return rmse, r2


def load_model_and_scaler():
    """
    Carga el modelo de AmesNet y el escalador.
    """
    model = AmesNet(input_dim=7)
    model.load_state_dict(torch.load(AMES_MODEL_FILENAME, map_location=torch.device("cpu"), weights_only=True))
    model.eval()
    scaler = joblib.load(SCALER_FILENAME)
    return model, scaler


def train_and_evaluate():
    """
    Entrena y evalúa el modelo AmesNet utilizando datos escalados y un DataLoader.
    """
    # Preparar datasets y escalador
    X_train, y_train = prepare_dataset("training")
    X_val, y_val = prepare_dataset("validation")
    X_train_scaled, X_val_scaled = scale_data(X_train, X_val)

    train_loader = create_dataloader(X_train_scaled, y_train, batch_size=BATCH_SIZE)
    val_loader = create_dataloader(X_val_scaled, y_val, batch_size=BATCH_SIZE, shuffle=False)

    # Inicializar modelo, pérdida y optimizador
    model = initialize_model(input_dim=X_train_scaled.shape[1])
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Entrenamiento
    train_model(model, train_loader, criterion, optimizer, epochs=50)

    # Guardar modelo
    save_model(model, AMES_MODEL_FILENAME)

    # Validación y evaluación
    rmse, r2 = validate_model(model, val_loader)
    return rmse, r2
