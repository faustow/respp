import os

import gradio as gr
import requests


# Función para predecir el precio estimado
def predict_price(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")

    PREDICTION_ENDPOINT = f"{django_url}/api/learning/predict-price/"
    data = {
        "lotarea": lotarea,
        "overallqual": overallqual,
        "overallcond": overallcond,
        "centralair": centralair,
        "fullbath": fullbath,
        "bedroomabvgr": bedroomabvgr,
        "garagecars": garagecars,
    }
    response = requests.post(PREDICTION_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json().get("predicted_price", "Error in prediction")
    return f"Error: {response.status_code}, {response.text}"


# Función para grabar una propiedad con el precio verificado
def record_price(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars, saleprice):
    django_url = os.getenv("DJANGO_PUBLIC_URL")
    if not django_url:
        raise ValueError("DJANGO_PUBLIC_URL is not set")
    CREATE_PROPERTY_ENDPOINT = f"{django_url}/api/properties/"
    data = {
        "lotarea": lotarea,
        "overallqual": overallqual,
        "overallcond": overallcond,
        "centralair": 1 if centralair == "Yes" else 0,
        "fullbath": fullbath,
        "bedroomabvgr": bedroomabvgr,
        "garagecars": garagecars,
        "saleprice": saleprice,
        "dataset": "user_submission",  # Indica que es un envío de usuario
        "data_source": 2,  # Verificado
    }
    response = requests.post(CREATE_PROPERTY_ENDPOINT, json=data)
    if response.status_code == 201:
        return response.json().get("message", "Property created successfully")
    return f"Error: {response.status_code}, {response.text}"


def create_ui():
    # Definir interfaces para Gradio
    with gr.Blocks() as app:
        gr.Markdown("### Sale Price Estimation and Recording UI")

        # Panel para predicción
        with gr.Row():
            gr.Markdown("#### Predict Sale Price")
            with gr.Column():
                lotarea = gr.Number(label="Lot Area", value=10000)
                overallqual = gr.Number(label="Overall Quality", value=7)
                overallcond = gr.Number(label="Overall Condition", value=5)
                centralair = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
                fullbath = gr.Number(label="Full Bathrooms", value=2)
                bedroomabvgr = gr.Number(label="Bedrooms Above Grade", value=3)
                garagecars = gr.Number(label="Garage Cars", value=2)
                predict_button = gr.Button("Predict Price")

            predicted_price = gr.Textbox(label="Predicted Price")

        predict_button.click(
            predict_price,
            inputs=[lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars],
            outputs=[predicted_price],
        )

        # Panel para grabar propiedad
        with gr.Row():
            gr.Markdown("#### Record Verified Sale Price")
            with gr.Column():
                lotarea_record = gr.Number(label="Lot Area", value=10000, precision=0, minimum=0)
                overallqual_record = gr.Number(label="Overall Quality", value=7, precision=0, minimum=0, maximum=10)
                overallcond_record = gr.Number(label="Overall Condition", value=5, precision=0, minimum=0)
                centralair_record = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
                fullbath_record = gr.Number(label="Full Bathrooms", value=2, precision=0, minimum=0)
                bedroomabvgr_record = gr.Number(label="Bedrooms Above Grade", value=3, precision=0, minimum=0)
                garagecars_record = gr.Number(label="Garage Cars", value=2, precision=0, minimum=0)
                saleprice_record = gr.Number(label="Verified Sale Price", value=250000, precision=0, minimum=0)
                record_button = gr.Button("Record Sale")

            record_message = gr.Textbox(label="Record Status")

        record_button.click(
            record_price,
            inputs=[
                lotarea_record,
                overallqual_record,
                overallcond_record,
                centralair_record,
                fullbath_record,
                bedroomabvgr_record,
                garagecars_record,
                saleprice_record,
            ],
            outputs=[record_message],
        )
    return app


# Ejecutar la aplicación
if __name__ == "__main__":
    app = create_ui()
    app.launch()
