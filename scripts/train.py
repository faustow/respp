import os
import sys

import django
import numpy as np
import pandas as pd
import torch
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from torch.utils.data import DataLoader, Dataset

# Añade el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Configura la variable de entorno para encontrar el archivo settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importa el modelo Property
from properties.models import Property

# Columns selected for training
SELECTED_COLUMNS = [
    "pid", "mssubclass", "mszoning", "lotarea", "overallqual", "overallcond",
    "yearbuilt", "yearremodadd", "grlivarea", "garagecars", "garagesqft",
    "totrmsabvgrd", "fullbath", "halfbath", "bedroomabvgr", "kitchenabvgr", "saleprice",
    "fireplaces", "heatingqc", "centralair", "exterqual", "bsmtfinsf1",
    "totalbsmtsf", "firstflrsf", "secondflrsf", "paveddrive", "openporchsf",
    "wooddecksf", "lotconfig", "neighborhood", "condition1", "housestyle",
]

# Columns omitted with reasons
OMITTED_COLUMNS = {
    "lotfrontage": "Missing ~18% of values; linear feet estimation uncertain.",
    "street": "Low variability; nearly all properties have paved access.",
    "alley": "Over 90% of values are missing.",
    "poolqc": "Pool quality rarely recorded (~99% missing).",
    "fence": "Fence information is incomplete (~80% missing).",
    "miscfeature": "Sparse information (~95% missing).",
    "roofmatl": "Rarely varies and minimally predictive.",
    "utilities": "Not significantly variable in this dataset.",
    "condition2": "Low variability and redundant with `condition1`.",
    "lowqualfinsf": "Very few values different from 0.",
    "threessnporch": "Rarely available information.",
    "miscval": "Not predictive; low and sparse values.",
    "lotshape": "Shape does not significantly affect sale price.",
    "landcontour": "Flatness of the property not strongly correlated with sale price.",
    "landslope": "Property slope is not strongly correlated with sale price.",
    "roofstyle": "Type of roof has low variability and minimal predictive power.",
    "bldgtype": "Building type is captured by other columns.",
    "masvnrtype": "High proportion of missing values (~40%).",
    "masvnrarea": "Strongly correlated with masonry type, leading to redundancy.",
    "extercond": "Condition of exterior material overlaps with quality.",
    "foundation": "Minimal variability and not predictive.",
    "bsmtqual": "Significant missing values (~30%).",
    "bsmtcond": "Significant missing values (~30%).",
    "bsmtexposure": "Significant missing values (~30%).",
    "bsmtfintype2": "Minimal impact on sale price; covered by `bsmtfintype1`.",
    "bsmtfinsf2": "Minimal impact on sale price; covered by `bsmtfinsf1`.",
    "bsmtunfsf": "Overlap with `totalbsmtsf`.",
    "electrical": "Low variability and minimal predictive power.",
    "functional": "Minimal impact on sale price.",
    "garagequal": "Garage quality overlaps with other garage features.",
    "garagecond": "Garage condition overlaps with other garage features.",
    "enclosedporch": "Minimal variability.",
    "screenporch": "Minimal variability.",
    "yrsold": "Year sold does not directly affect property characteristics.",
    "mosold": "Month sold has minimal predictive power.",
    "saletype": "Type of sale has minimal predictive power.",
    "salecondition": "Condition of sale overlaps with other features."
}


def fetch_data():
    """
    Fetch data from the Property model and preprocess it for training.
    """
    queryset = Property.objects.values(*SELECTED_COLUMNS)
    data = []
    labels = []

    for record in queryset:
        label = record.pop("saleprice", None)
        if label is not None:
            data.append(record)
            labels.append(label)

    data = pd.DataFrame(data)

    # Handle missing values
    imputer = SimpleImputer(strategy="most_frequent")
    data = imputer.fit_transform(data)

    # Handle categorical variables
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    data = encoder.fit_transform(data)

    return np.array(data, dtype=np.float32), np.array(labels, dtype=np.float32)


# Custom Dataset for PyTorch
class AmesDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


# Model Definition
class AmesNet(torch.nn.Module):
    def __init__(self, input_dim):
        super(AmesNet, self).__init__()
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)


# Training Function
def train_model():
    # Fetch data
    data, labels = fetch_data()

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    # Create datasets and dataloaders
    train_dataset = AmesDataset(X_train, y_train)
    test_dataset = AmesDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32)

    # Initialize model
    model = AmesNet(input_dim=data.shape[1])
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Training loop
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

    # Save model
    torch.save(model.state_dict(), "ames_model.pth")
    print("Model saved to 'ames_model.pth'.")

    # Evaluate model
    model.eval()
    with torch.no_grad():
        total_loss = 0
        for batch_data, batch_labels in test_loader:
            predictions = model(batch_data).squeeze()
            loss = criterion(predictions, batch_labels)
            total_loss += loss.item()
        print(f"Test Loss: {total_loss / len(test_loader):.4f}")


# Run training
if __name__ == "__main__":
    train_model()
