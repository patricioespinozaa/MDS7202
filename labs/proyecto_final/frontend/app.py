import gradio as gr
from services import enviar_prediccion

CANALES = ["Whatsapp", "Correo", "Página Web"]
CATEGORIAS_PROBLEMA = ["Cuenta", "Fraude", "Técnica", "Cobros", "Pregunta general", "Otro"]

tema = gr.themes.Soft(primary_hue="sky", secondary_hue="purple")


def _predecir(asunto_ticket, contenido_ticket, canal_ticket, categoria_problema):
    if not asunto_ticket.strip() or not contenido_ticket.strip():
        return "Debe completar el asunto y el contenido del ticket."

    return enviar_prediccion(
        asunto_ticket=asunto_ticket,
        contenido_ticket=contenido_ticket,
        canal_ticket=canal_ticket,
        categoria_problema=categoria_problema,
    )


with gr.Blocks(title="ChaucherApp. Priorización de Tickets") as demo:
    gr.Markdown("# ChaucherApp")
    gr.Markdown("Sistema de priorización de tickets de soporte al cliente.")

    gr.Markdown("### Datos del ticket")
    asunto_ticket = gr.Textbox(label="Asunto del ticket")
    contenido_ticket = gr.Textbox(label="Contenido del ticket", lines=5)

    gr.Markdown("### Clasificación del ticket")
    canal_ticket = gr.Dropdown(choices=CANALES, value=CANALES[0], label="Canal de ingreso")
    categoria_problema = gr.Dropdown(
        choices=CATEGORIAS_PROBLEMA, value=CATEGORIAS_PROBLEMA[0], label="Categoría del problema"
    )

    boton_predecir = gr.Button("Predecir prioridad", variant="primary")
    resultado = gr.Textbox(label="Nivel de prioridad", interactive=False)

    boton_predecir.click(
        fn=_predecir,
        inputs=[asunto_ticket, contenido_ticket, canal_ticket, categoria_problema],
        outputs=resultado,
    )


if __name__ == "__main__":
    demo.launch(theme=tema, server_name="0.0.0.0", server_port=7860)
