import gradio as gr

from ui.apis import record_price


def create_sale_recording_panel():
    with gr.Row():
        gr.Markdown("### Record Verified Sale Price")
        with gr.Column():
            lotarea_record = gr.Number(label="Lot Area", value=10000, precision=0, minimum=0)
            overallqual_record = gr.Number(label="Overall Quality", value=7, precision=0, minimum=0, maximum=10)
            overallcond_record = gr.Number(label="Overall Condition", value=5, precision=0, minimum=0)
            centralair_record = gr.Radio(["Yes", "No"], label="Central Air", value="Yes")
            fullbath_record = gr.Number(label="Full Bathrooms", value=2, precision=0, minimum=0)
            bedroomabvgr_record = gr.Number(label="Bedrooms Above Grade", value=3, precision=0, minimum=0)
            garagecars_record = gr.Number(label="Garage Cars", value=2, precision=0, minimum=0)
            saleprice_record = gr.Number(label="Verified Sale Price", value=250000, precision=0, minimum=0)
            record_button = gr.Button("Record Sale")

        record_message = gr.Textbox(label="Record Status")
    record_button.click(
        record_price,
        inputs=[
            lotarea_record,
            overallqual_record,
            overallcond_record,
            centralair_record,
            fullbath_record,
            bedroomabvgr_record,
            garagecars_record,
            saleprice_record,
        ],
        outputs=[record_message],
    )
