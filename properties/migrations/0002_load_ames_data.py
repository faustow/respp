import os

import numpy as np
import pandas as pd
from django.db import migrations

from config.settings import GLOBAL_SEED


def load_ames_data(apps, schema_editor):
    Property = apps.get_model("properties", "Property")

    file_path = os.path.join(os.path.dirname(__file__), '../data/ames_housing.csv')

    data = pd.read_csv(file_path)

    # Mapear `centralair` de texto a booleano
    data["centralair"] = data["Central Air"].map({"Y": 1, "N": 0}).fillna(0)

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
            pid=row['PID'],
            mssubclass=row['MS SubClass'],
            mszoning=row['MS Zoning'],
            lotfrontage=row['Lot Frontage'] if pd.notna(row['Lot Frontage']) else None,
            lotarea=row['Lot Area'],
            street=row['Street'],
            alley=row['Alley'] if pd.notna(row['Alley']) else None,
            lotshape=row['Lot Shape'],
            landcontour=row['Land Contour'],
            utilities=row['Utilities'],
            lotconfig=row['Lot Config'],
            landslope=row['Land Slope'],
            neighborhood=row['Neighborhood'],
            condition1=row['Condition 1'],
            condition2=row['Condition 2'],
            bldgtype=row['Bldg Type'],
            housestyle=row['House Style'],
            overallqual=row['Overall Qual'],
            overallcond=row['Overall Cond'],
            yearbuilt=row['Year Built'],
            yearremodadd=row['Year Remod/Add'],
            roofstyle=row['Roof Style'],
            roofmatl=row['Roof Matl'],
            exterior1st=row['Exterior 1st'],
            exterior2nd=row['Exterior 2nd'],
            masvnrtype=row['Mas Vnr Type'] if pd.notna(row['Mas Vnr Type']) else None,
            masvnrarea=row['Mas Vnr Area'] if pd.notna(row['Mas Vnr Area']) else None,
            exterqual=row['Exter Qual'],
            extercond=row['Exter Cond'],
            foundation=row['Foundation'],
            bsmtqual=row['Bsmt Qual'] if pd.notna(row['Bsmt Qual']) else None,
            bsmtcond=row['Bsmt Cond'] if pd.notna(row['Bsmt Cond']) else None,
            bsmtexposure=row['Bsmt Exposure'] if pd.notna(row['Bsmt Exposure']) else None,
            bsmtfintype1=row['BsmtFin Type 1'] if pd.notna(row['BsmtFin Type 1']) else None,
            bsmtfinsf1=row['BsmtFin SF 1'] if pd.notna(row['BsmtFin SF 1']) else None,
            bsmtfintype2=row['BsmtFin Type 2'] if pd.notna(row['BsmtFin Type 2']) else None,
            bsmtfinsf2=row['BsmtFin SF 2'] if pd.notna(row['BsmtFin SF 2']) else None,
            bsmtunfsf=row['Bsmt Unf SF'] if pd.notna(row['Bsmt Unf SF']) else None,
            totalbsmtsf=row['Total Bsmt SF'] if pd.notna(row['Total Bsmt SF']) else None,
            heating=row['Heating'],
            heatingqc=row['Heating QC'],
            centralair=row['centralair'],
            electrical=row['Electrical'] if pd.notna(row['Electrical']) else None,
            firstflrsf=row['1st Flr SF'],
            secondflrsf=row['2nd Flr SF'],
            lowqualfinsf=row['Low Qual Fin SF'],
            grlivarea=row['Gr Liv Area'],
            bsmtfullbath=row['Bsmt Full Bath'] if pd.notna(row['Bsmt Full Bath']) else None,
            bsmthalfbath=row['Bsmt Half Bath'] if pd.notna(row['Bsmt Half Bath']) else None,
            fullbath=row['Full Bath'],
            halfbath=row['Half Bath'],
            bedroomabvgr=row['Bedroom AbvGr'],
            kitchenabvgr=row['Kitchen AbvGr'],
            kitchenqual=row['Kitchen Qual'],
            totrmsabvgrd=row['TotRms AbvGrd'],
            functional=row['Functional'],
            fireplaces=row['Fireplaces'],
            fireplacequ=row['Fireplace Qu'] if pd.notna(row['Fireplace Qu']) else None,
            garagetype=row['Garage Type'] if pd.notna(row['Garage Type']) else None,
            garageyrblt=row['Garage Yr Blt'] if pd.notna(row['Garage Yr Blt']) else None,
            garagefinish=row['Garage Finish'] if pd.notna(row['Garage Finish']) else None,
            garagecars=row['Garage Cars'] if pd.notna(row['Garage Cars']) else None,
            garagesqft=row['Garage Area'] if pd.notna(row['Garage Area']) else None,
            garagequal=row['Garage Qual'] if pd.notna(row['Garage Qual']) else None,
            garagecond=row['Garage Cond'] if pd.notna(row['Garage Cond']) else None,
            paveddrive=row['Paved Drive'],
            wooddecksf=row['Wood Deck SF'],
            openporchsf=row['Open Porch SF'],
            enclosedporch=row['Enclosed Porch'],
            threessnporch=row['3Ssn Porch'],
            screenporch=row['Screen Porch'],
            poolarea=row['Pool Area'],
            poolqc=row['Pool QC'] if pd.notna(row['Pool QC']) else None,
            fence=row['Fence'] if pd.notna(row['Fence']) else None,
            miscfeature=row['Misc Feature'] if pd.notna(row['Misc Feature']) else None,
            miscval=row['Misc Val'],
            mosold=row['Mo Sold'],
            yrsold=row['Yr Sold'],
            saletype=row['Sale Type'],
            salecondition=row['Sale Condition'],
            saleprice=row['SalePrice'],
            data_source=1,  # Ames dataset
            dataset=row["dataset_type"],
        )


def reverse_func(apps, schema_editor):
    Property = apps.get_model("properties", "Property")
    Property.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_ames_data, reverse_func),
    ]
