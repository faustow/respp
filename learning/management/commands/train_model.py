from django.core.management.base import BaseCommand

from learning.training import train_model


class Command(BaseCommand):
    help = 'Train the AmesNet model using the dataset'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the training process...')
        train_model()
        self.stdout.write('Training process completed successfully.')
