"""App de Gradio para priorizar tickets de soporte de ChaucherApp."""

import gradio as gr
from services import enviar_prediccion

# Paleta acorde a la estética de ChaucherApp: celeste + morado claro.
CELESTE = "#3AB6E8"
MORADO_CLARO = "#B39DDB"

CANALES = ["Whatsapp", "Correo", "Página Web"]
CATEGORIAS_PROBLEMA = ["Cuenta", "Fraude", "Técnica", "Cobros", "Pregunta general", "Otro"]

COLOR_POR_PRIORIDAD = {
    "Baja": "#4CAF50",
    "Media": "#FFC107",
    "Alta": "#FF9800",
    "Critica": "#E53935",
}

CSS = f"""
.gradio-container {{
    background: linear-gradient(135deg, {CELESTE}14 0%, {MORADO_CLARO}14 100%);
}}
#titulo {{
    text-align: center;
    background: linear-gradient(90deg, {CELESTE} 0%, {MORADO_CLARO} 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
}}
#titulo h1 {{
    margin: 0;
    font-size: 1.6em;
}}
#titulo p {{
    margin: 4px 0 0 0;
    font-size: 1em;
    opacity: 0.9;
}}
"""

tema = gr.themes.Soft(primary_hue="purple", secondary_hue="sky")


def _predecir(asunto_ticket, contenido_ticket, canal_ticket, categoria_problema):
    if not asunto_ticket.strip() or not contenido_ticket.strip():
        return "Debe completar el asunto y el contenido del ticket."

    resultado = enviar_prediccion(
        asunto_ticket=asunto_ticket,
        contenido_ticket=contenido_ticket,
        canal_ticket=canal_ticket,
        categoria_problema=categoria_problema,
    )

    if resultado.startswith("Error") or resultado.startswith("No se pudo"):
        return resultado

    color = COLOR_POR_PRIORIDAD.get(resultado, "#607D8B")
    return (
        f'<div style="background:{color}22; border:2px solid {color}; '
        f'border-radius:10px; padding:16px; text-align:center;">'
        f'<span style="font-size:1.1em;">Prioridad predicha:</span><br>'
        f'<span style="font-size:1.8em; font-weight:bold; color:{color};">{resultado}</span>'
        f"</div>"
    )


with gr.Blocks(title="ChaucherApp. Priorización de Tickets") as demo:
    gr.HTML(
        '<div id="titulo">'
        "<h1>ChaucherApp</h1>"
        "<p>Sistema de priorización de tickets de soporte al cliente</p>"
        "</div>"
    )
    gr.Markdown("Complete los datos del ticket para obtener el nivel de prioridad estimado.")

    with gr.Group():
        gr.Markdown("### Descripción del ticket")
        asunto_ticket = gr.Textbox(label="Asunto del ticket", placeholder="Ejemplo: Transferencia fallida")
        contenido_ticket = gr.Textbox(
            label="Contenido del ticket",
            placeholder="Describa el problema con el mayor detalle posible.",
            lines=5,
        )

    with gr.Group():
        gr.Markdown("### Clasificación del ticket")
        with gr.Row():
            canal_ticket = gr.Dropdown(choices=CANALES, value=CANALES[0], label="Canal de ingreso")
            categoria_problema = gr.Dropdown(
                choices=CATEGORIAS_PROBLEMA, value=CATEGORIAS_PROBLEMA[0], label="Categoría del problema"
            )

    boton_predecir = gr.Button("Predecir prioridad", variant="primary")
    resultado_html = gr.HTML()

    boton_predecir.click(
        fn=_predecir,
        inputs=[asunto_ticket, contenido_ticket, canal_ticket, categoria_problema],
        outputs=resultado_html,
    )


if __name__ == "__main__":
    demo.launch(theme=tema, css=CSS, server_name="0.0.0.0", server_port=7860)
