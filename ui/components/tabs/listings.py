import gradio as gr

from ui.components.panels.customer_profiles import create_customer_profiles_panel
from ui.components.panels.listing import create_listing_panel
from ui.components.panels.search import create_search_panel


def create_sales_listing_tab(prediction_data_state):
    """
    Crea la pestaña "Sales Listing and Customer Profiling UI".
    """
    with gr.Blocks() as tab:
        gr.Markdown("## Sales Listing and Customer Profiling UI")

        # Panel de búsqueda
        gr.Markdown("### Search for Closest Property")
        search_results, search_panel = create_search_panel(prediction_data_state)

        gr.Markdown("---")

        # Panel para generación de listings
        gr.Markdown("### Generate Sales Listing for the Property")
        listing_panel = create_listing_panel(search_results, prediction_data_state)

        gr.Markdown("---")

        # Panel para generación de perfiles de cliente
        gr.Markdown("### Generate Customer Profiles for the Listing")
        customer_profiles_panel = create_customer_profiles_panel(prediction_data_state)

        # Agregar paneles al bloque
        search_panel
        listing_panel
        customer_profiles_panel

        return tab

    return tab
