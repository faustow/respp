import gradio as gr

from ui.apis import generate_listing, vote_listing


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
