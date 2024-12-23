import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from properties.models import Property

# Columns selected for training
SELECTED_COLUMNS = [
    "lotarea", "overallqual", "overallcond", "centralair", "fullbath", "bedroomabvgr", "garagecars", "saleprice"
]


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
