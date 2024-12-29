import gradio as gr

from ui.apis import predict_price


def create_prediction_panel(prediction_data_state):
    with gr.Row():
        gr.Markdown("### Predict Sale Price")
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

    def store_prediction_data(lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars):
        """Guarda los datos ingresados en un estado compartido."""
        return {
            "lotarea": lotarea,
            "overallqual": overallqual,
            "overallcond": overallcond,
            "centralair": 1 if centralair == "Yes" else 0,
            "fullbath": fullbath,
            "bedroomabvgr": bedroomabvgr,
            "garagecars": garagecars,
        }

    predict_button.click(
        predict_price,
        inputs=[lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars],
        outputs=[predicted_price],
    )
    predict_button.click(
        store_prediction_data,
        inputs=[lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars],
        outputs=[prediction_data_state],
    )
