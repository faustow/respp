import gradio as gr

from ui.apis import search_property, generate_listing, vote_listing


def create_search_panel(listing_id_state):
    """Crea el panel para búsqueda de propiedades."""
    with gr.Row(equal_height=True):  # Hacer las columnas de igual altura
        with gr.Column(scale=2):  # Ampliar el espacio para los inputs
            search_lotarea = gr.Number(label="Lot Area", value=10000)
            search_overallqual = gr.Number(label="Overall Quality", value=7)
            search_overallcond = gr.Number(label="Overall Condition", value=5)
            search_centralair = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
            search_fullbath = gr.Number(label="Full Bathrooms", value=2)
            search_bedroomabvgr = gr.Number(label="Bedrooms Above Grade", value=3)
            search_garagecars = gr.Number(label="Garage Cars", value=2)
            search_button = gr.Button("Search Property")
        with gr.Column(scale=3):  # Más espacio para los resultados
            search_results = gr.JSON(label="Closest Property")  # Eliminamos interactive=False

    search_button.click(
        search_property,
        inputs=[
            search_lotarea,
            search_overallqual,
            search_overallcond,
            search_centralair,
            search_fullbath,
            search_bedroomabvgr,
            search_garagecars,
        ],
        outputs=[search_results],
    )

    return search_results, gr.Row([
        gr.Column([search_lotarea, search_overallqual, search_overallcond,
                   search_centralair, search_fullbath, search_bedroomabvgr, search_garagecars, search_button]),
        gr.Column([search_results]),
    ])


def create_listing_panel(search_results, listing_id_state):
    """Crea el panel para generar un listing de ventas."""
    with gr.Row(equal_height=True):
        with gr.Column(scale=3):  # Ampliar espacio para inputs y resultados
            description_input = gr.Textbox(
                label="Description",
                placeholder="Enter the best features of the property...",
                lines=3,
            )
            generate_button = gr.Button("Generate Listing")
            generated_text_output = gr.Textbox(
                label="Generated Listing",
                placeholder="The generated salesy listing will appear here...",
                lines=5,
                interactive=False,
            )
        with gr.Column(scale=1):  # Reducir el espacio para votos
            thumbs_up_button = gr.Button("👍 Thumbs Up")
            thumbs_down_button = gr.Button("👎 Thumbs Down")
            voting_message = gr.Textbox(label="Voting Status", interactive=False)

    def handle_generated_response(response):
        """Procesa la respuesta generada para extraer el listing_id y el texto generado."""
        listing_id = response.get("id")  # Corrected key for listing_id
        generated_text = response.get("generated_text", "No text generated.")
        return generated_text, listing_id

    generate_button.click(
        generate_listing,
        inputs=[description_input, search_results],
        outputs=[generated_text_output, listing_id_state],
        postprocess=handle_generated_response,
    )

    thumbs_up_button.click(
        lambda listing_id: vote_listing(1, listing_id),
        inputs=[listing_id_state],
        outputs=[voting_message],
    )

    thumbs_down_button.click(
        lambda listing_id: vote_listing(-1, listing_id),
        inputs=[listing_id_state],
        outputs=[voting_message],
    )

    return gr.Row([
        gr.Column([description_input, generate_button, generated_text_output], scale=3),
        gr.Column([thumbs_up_button, thumbs_down_button, voting_message], scale=1),
    ])


def create_customer_profiles_panel(listing_id_state):
    """Crea el panel para generar perfiles de cliente para un listado específico."""
    with gr.Row():
        generate_profiles_button = gr.Button("Generate Customer Profiles")
        user_profiles_output = gr.Textbox(
            label="Customer Profiles",
            placeholder="The generated customer profiles will appear here...",
            lines=10,
            interactive=False,
        )

    def handle_generate_profiles(listing_id):
        """Genera perfiles de clientes utilizando el listing_id."""
        if not listing_id:
            return "Error: No listing selected. Please generate a listing first."
        from ui.apis import get_customer_profiles
        response = get_customer_profiles(listing_id)
        if isinstance(response, str):  # Si hubo un error
            return response
        formatted_profiles = "\n\n".join(
            [f"Occupation: {p['occupation']}, Income: {p['annual_income']}, Reason: {p['reason']}" for p in response]
        )
        return formatted_profiles

    generate_profiles_button.click(
        handle_generate_profiles,
        inputs=[listing_id_state],
        outputs=[user_profiles_output],
    )

    return gr.Row([generate_profiles_button, user_profiles_output])


def create_sales_listing_tab():
    """
    Ensambla la pestaña "Sales Listing and Customer Profiling UI".
    """
    with gr.Blocks() as tab:
        gr.Markdown("## Sales Listing and Customer Profiling UI")

        # Estado compartido para el listing_id
        listing_id_state = gr.State()

        # Panel de búsqueda
        gr.Markdown("### Search for Closest Property")
        search_results, search_panel = create_search_panel(listing_id_state)

        gr.Markdown("---")

        # Panel para generación de listings
        gr.Markdown("### Generate Sales Listing for the Property")
        listing_panel = create_listing_panel(search_results, listing_id_state)

        gr.Markdown("---")

        # Panel para generación de perfiles de cliente
        gr.Markdown("### Generate Customer Profiles for the Listing")
        customer_profiles_panel = create_customer_profiles_panel(listing_id_state)

        # Agregar paneles al bloque
        search_panel
        listing_panel
        customer_profiles_panel

    return tab
