import os
import uuid

import numpy as np
import pandas as pd
from django.db import migrations

from config.settings import GLOBAL_SEED


def load_ames_data(apps, schema_editor):
    Property = apps.get_model("properties", "Property")

    file_path = os.path.join(os.path.dirname(__file__), '../data/ames_housing.csv')

    data = pd.read_csv(file_path)

    # Mapear `centralair` de texto a booleano
    data["centralair"] = data["Central Air"].map({"Y": True, "N": False}).fillna(False)

    # Hacer el split reproducible
    np.random.seed(GLOBAL_SEED)
    data["dataset_type"] = np.random.choice(
        ["training", "validation", "test"],
        size=len(data),
        p=[0.7, 0.15, 0.15],  # 70% training, 15% validation, 15% test
    )

    # Insertar los datos en la base de datos
    for _, row in data.iterrows():
        Property.objects.create(
            id=uuid.uuid4(),
            pid=row["PID"],
            lotarea=row["Lot Area"],
            overallqual=row["Overall Qual"],
            overallcond=row["Overall Cond"],
            centralair=row["centralair"],
            fullbath=row["Full Bath"],
            bedroomabvgr=row["Bedroom AbvGr"],
            garagecars=row["Garage Cars"] if pd.notnull(row["Garage Cars"]) else 0,
            saleprice=row["SalePrice"],
            data_source=1,  # Ames dataset
            dataset=row["dataset_type"],
        )


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_ames_data),
    ]
