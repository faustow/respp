import gradio as gr

from ui.components.tabs.estimation import create_price_estimation_tab
from ui.components.tabs.listings import create_sales_listing_tab
from ui.components.toggle import create_theme_toggle


def create_ui():
    """
    Ensambla la interfaz de usuario con las diferentes pestañas.
    """

    def switch_theme(theme):
        """Genera el HTML necesario para redirigir a la página con el tema seleccionado."""
        return f'<meta http-equiv="refresh" content="0; url=?__theme={theme}">'

    with gr.Blocks() as app:
        gr.Markdown("# Real Estate Sales Assistant")

        # Pestaña de listing usando estado compartido
        create_theme_toggle(switch_theme)
        with gr.Tab("Sale Price Estimation and Recording"):
            estimation_tab, prediction_data_state = create_price_estimation_tab()
        with gr.Tab("Sales Listing and Customer Profiling"):
            listing_tab = create_sales_listing_tab(prediction_data_state)

    return app


# Ejecutar la aplicación
if __name__ == "__main__":
    app = create_ui()
    app.launch()
