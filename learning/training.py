import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset

from .datasets import fetch_data
from .models import AmesNet


class AmesDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


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
