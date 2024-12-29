import gradio as gr


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
