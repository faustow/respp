import gradio as gr

from ui.apis import search_property, generate_listing, vote_listing


def create_sales_listing_tab():
    """
    Crea la pestaña de "Sales Listing and Customer Profiling UI".
    """
    with gr.Blocks() as tab:
        gr.Markdown("### Sales Listing and Customer Profiling UI")

        # Panel para búsqueda
        with gr.Row():
            gr.Markdown("#### Search for Closest Property")
            with gr.Column():
                search_lotarea = gr.Number(label="Lot Area", value=10000)
                search_overallqual = gr.Number(label="Overall Quality", value=7)
                search_overallcond = gr.Number(label="Overall Condition", value=5)
                search_centralair = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
                search_fullbath = gr.Number(label="Full Bathrooms", value=2)
                search_bedroomabvgr = gr.Number(label="Bedrooms Above Grade", value=3)
                search_garagecars = gr.Number(label="Garage Cars", value=2)
                search_button = gr.Button("Search Property")
                copy_button = gr.Button("Copy Values from Estimation UI")

            search_results = gr.JSON(label="Closest Property")
            listing_id_state = gr.State()  # Variable para almacenar el listing_id

        # Consulta de búsqueda
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

        # Panel para generación de listings
        gr.Markdown("#### Generate Sales Listing for the Property")
        with gr.Row():
            with gr.Column():
                description_input = gr.Textbox(
                    label="Description",
                    placeholder="Enter the best features of the property...",
                    lines=3
                )
                generate_button = gr.Button("Generate Listing")
                feedback_message = gr.Textbox(label="Feedback", interactive=False)
            with gr.Column():
                generated_text_output = gr.Textbox(
                    label="Generated Listing",
                    placeholder="The generated salesy listing will appear here...",
                    lines=5,
                    interactive=False
                )
                thumbs_up_button = gr.Button("👍 Thumbs Up")
                thumbs_down_button = gr.Button("👎 Thumbs Down")
                voting_message = gr.Textbox(label="Voting Status", interactive=False)

        # Función para procesar la respuesta del backend
        def handle_generated_response(response):
            """Parses the generated response to extract the listing_id and generated text."""
            listing_id = response.get("listing_id")
            generated_text = response.get("generated_text", "No text generated.")
            return generated_text, listing_id

        # Conectar el botón de generación con la función
        generate_button.click(
            generate_listing,
            inputs=[description_input, search_results],
            outputs=[generated_text_output, listing_id_state],
            postprocess=handle_generated_response,
        )

        # Conectar los botones de votos con la función
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

    return tab
