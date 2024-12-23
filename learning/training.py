import numpy as np
import torch
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset

from .models import AmesNet


class AmesDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


def train_and_evaluate(data, labels, model_path="ames_model.pth"):
    """
    Train the model and evaluate it.
    Returns metrics: MSE and R^2.
    """
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    # Create datasets and dataloaders
    train_dataset = AmesDataset(X_train, y_train)
    test_dataset = AmesDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32)

    # Initialize the model
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

    # Save the model
    torch.save(model.state_dict(), model_path)
    np.save("data_test.npy", X_test)
    np.save("labels_test.npy", y_test)

    print(f"Model saved to '{model_path}'.")

    # Evaluation
    model.eval()
    with torch.no_grad():
        predictions = []
        true_labels = []
        for batch_data, batch_labels in test_loader:
            preds = model(batch_data).squeeze()
            predictions.extend(preds.numpy())
            true_labels.extend(batch_labels.numpy())

    mse = mean_squared_error(true_labels, predictions)
    r2 = r2_score(true_labels, predictions)

    print(f"Test Loss (MSE): {mse:.4f}")
    print(f"R^2 Score: {r2:.4f}")

    return mse, r2
