import numpy as np
import torch
from django.core.management.base import BaseCommand

from learning.datasets import fetch_data
from learning.training import train_and_evaluate


class Command(BaseCommand):
    help = "Train the AmesNet model using the dataset"

    def handle(self, *args, **kwargs):
        # Set global seeds
        torch.manual_seed(42)
        np.random.seed(42)

        self.stdout.write("Starting the training process...")
        rmse, r2 = train_and_evaluate()

        self.stdout.write(f"Training completed. RMSE: {rmse:.4f}, R^2: {r2:.4f}")
