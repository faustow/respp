import gradio as gr

from ui.components.estimation import create_price_estimation_tab
from ui.components.listings import create_sales_listing_tab


def create_ui():
    """
    Ensambla la interfaz de usuario con las diferentes pestañas.
    """
    with gr.Blocks() as app:
        with gr.Tab("Sale Price Estimation and Recording"):
            tab1 = create_price_estimation_tab()
        with gr.Tab("Sales Listing and Customer Profiling"):
            tab2 = create_sales_listing_tab()

    return app


# Ejecutar la aplicación
if __name__ == "__main__":
    app = create_ui()
    app.launch()
