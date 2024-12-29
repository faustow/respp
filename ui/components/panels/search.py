import gradio as gr

from ui.apis import search_property


def create_search_panel(prediction_data_state):
    """Crea el panel para búsqueda de propiedades."""
    with gr.Row():
        gr.Markdown("#### Search for Closest Property")
        with gr.Column():
            lotarea = gr.Number(label="Lot Area", value=10000)
            overallqual = gr.Number(label="Overall Quality", value=7)
            overallcond = gr.Number(label="Overall Condition", value=5)
            centralair = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
            fullbath = gr.Number(label="Full Bathrooms", value=2)
            bedroomabvgr = gr.Number(label="Bedrooms Above Grade", value=3)
            garagecars = gr.Number(label="Garage Cars", value=2)
            search_button = gr.Button("Search Property")
            copy_button = gr.Button("Copy from Prediction Form")  # Nuevo botón

        search_results = gr.JSON(label="Search Results")

    def copy_from_prediction(prediction_data):
        """Copia los datos desde el estado compartido hacia el formulario de búsqueda."""
        if prediction_data:
            return (
                prediction_data.get("lotarea", 10000),
                prediction_data.get("overallqual", 7),
                prediction_data.get("overallcond", 5),
                "Yes" if prediction_data.get("centralair", 1) else "No",
                prediction_data.get("fullbath", 2),
                prediction_data.get("bedroomabvgr", 3),
                prediction_data.get("garagecars", 2),
            )
        return 10000, 7, 5, "Yes", 2, 3, 2

    copy_button.click(
        copy_from_prediction,
        inputs=[prediction_data_state],
        outputs=[lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars],
    )

    search_button.click(
        search_property,
        inputs=[lotarea, overallqual, overallcond, centralair, fullbath, bedroomabvgr, garagecars],
        outputs=[search_results],
    )

    return search_results, gr.Row([
        gr.Column([lotarea, overallqual, overallcond,
                   centralair, fullbath, bedroomabvgr, garagecars, search_button]),
        gr.Column([search_results]),
    ])
