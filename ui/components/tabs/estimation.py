import gradio as gr

from ui.components.panels.prediction import create_prediction_panel
from ui.components.panels.sale_recording import create_sale_recording_panel


def create_price_estimation_tab():
    """
    Crea la pestaña de "Sale Price Estimation and Recording UI".
    """
    with gr.Blocks() as tab:
        gr.Markdown("## Sale Price Estimation and Recording UI")

        # Estado compartido para guardar datos de predicción
        prediction_data_state = gr.State()

        # Panel para predicción
        create_prediction_panel(prediction_data_state)

        gr.Markdown("---")

        # Panel para grabar propiedad
        create_sale_recording_panel()
    return tab, prediction_data_state
