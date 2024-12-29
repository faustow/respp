import gradio as gr


def create_theme_toggle(switch_theme):
    """
    Creates a theme toggle button to switch between Gradio's Light and Dark themes.
    """
    with gr.Row():
        with gr.Column():
            pass

        with gr.Column():
            pass

        with gr.Column():
            pass

        with gr.Column():
            dark_button = gr.Button("Dark Mode", size="sm")
            light_button = gr.Button("Light Mode", size="sm")
            theme_output = gr.HTML()  # Salida para redirección HTML

            dark_button.click(
                fn=lambda: switch_theme("dark"), inputs=[], outputs=[theme_output]
            )
            light_button.click(
                fn=lambda: switch_theme("light"), inputs=[], outputs=[theme_output]
            )
