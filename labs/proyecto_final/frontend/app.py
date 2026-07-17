import gradio as gr
from services import enviar_prediccion

tema = gr.themes.Soft(primary_hue="sky", secondary_hue="purple")


def _predecir(asunto_ticket, contenido_ticket):
    if not asunto_ticket.strip() or not contenido_ticket.strip():
        return "Debe completar el asunto y el contenido del ticket."

    return enviar_prediccion(asunto_ticket=asunto_ticket, contenido_ticket=contenido_ticket)


with gr.Blocks(title="ChaucherApp. Priorización de Tickets") as demo:
    gr.Markdown("# ChaucherApp")
    gr.Markdown("Sistema de priorización de tickets de soporte al cliente.")

    gr.Markdown("### Datos del ticket")
    asunto_ticket = gr.Textbox(label="Asunto del ticket")
    contenido_ticket = gr.Textbox(label="Contenido del ticket", lines=5)

    boton_predecir = gr.Button("Predecir prioridad", variant="primary")
    resultado = gr.Textbox(label="Nivel de prioridad", interactive=False)

    boton_predecir.click(
        fn=_predecir,
        inputs=[asunto_ticket, contenido_ticket],
        outputs=resultado,
    )


if __name__ == "__main__":
    demo.launch(theme=tema, server_name="0.0.0.0", server_port=7860)
