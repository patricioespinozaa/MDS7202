import gradio as gr
from services import enviar_prediccion

# Paleta de colores
CELESTE = "#3AB6E8"
MORADO_CLARO = "#B39DDB"

CANALES = ["Whatsapp", "Correo", "Página Web"]
CATEGORIAS_PROBLEMA = ["Cuenta", "Fraude", "Técnica", "Cobros", "Pregunta general", "Otro"]
TIPOS_CUENTA = ["Free", "Premium", "Business"]

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
    padding: 18px;
    border-radius: 12px;
    color: white;
}}
"""

tema = gr.themes.Soft(primary_hue="purple", secondary_hue="sky")


def _predecir(
    asunto_ticket,
    contenido_ticket,
    canal_ticket,
    categoria_problema,
    usuario_tipo_cuenta,
    usuario_antiguedad_dias,
):
    if not asunto_ticket.strip() or not contenido_ticket.strip():
        return "⚠️ Debes completar el asunto y el contenido del ticket."

    resultado = enviar_prediccion(
        asunto_ticket=asunto_ticket,
        contenido_ticket=contenido_ticket,
        canal_ticket=canal_ticket,
        categoria_problema=categoria_problema,
        usuario_tipo_cuenta=usuario_tipo_cuenta,
        usuario_antiguedad_dias=int(usuario_antiguedad_dias),
    )

    if resultado.startswith("⚠️"):
        return resultado

    color = COLOR_POR_PRIORIDAD.get(resultado, "#607D8B")
    return (
        f'<div style="background:{color}22; border:2px solid {color}; '
        f'border-radius:10px; padding:16px; text-align:center;">'
        f'<span style="font-size:1.1em;">Prioridad predicha:</span><br>'
        f'<span style="font-size:1.8em; font-weight:bold; color:{color};">{resultado}</span>'
        f"</div>"
    )


with gr.Blocks(title="ChaucherApp - Priorización de Tickets") as demo:
    gr.HTML('<h1 id="titulo">🎫 ChaucherApp — Priorización de Tickets de Soporte</h1>')
    gr.Markdown("Completa los datos del ticket y del usuario para predecir su nivel de prioridad.")

    with gr.Group():
        gr.Markdown("### 🎫 Atributos del Ticket")
        asunto_ticket = gr.Textbox(label="Asunto del ticket", placeholder="Ej: Transferencia fallida")
        contenido_ticket = gr.Textbox(
            label="Contenido del ticket",
            placeholder="Describe el problema con el mayor detalle posible...",
            lines=5,
        )
        with gr.Row():
            canal_ticket = gr.Dropdown(choices=CANALES, value=CANALES[0], label="Canal de ingreso")
            categoria_problema = gr.Dropdown(
                choices=CATEGORIAS_PROBLEMA, value=CATEGORIAS_PROBLEMA[0], label="Categoría del problema"
            )

    with gr.Group():
        gr.Markdown("### 👤 Atributos del Usuario")
        with gr.Row():
            usuario_tipo_cuenta = gr.Dropdown(choices=TIPOS_CUENTA, value=TIPOS_CUENTA[0], label="Tipo de cuenta")
            usuario_antiguedad_dias = gr.Number(
                label="Antigüedad de la cuenta (días)", value=30, minimum=0, precision=0
            )

    boton_predecir = gr.Button("🔮 Predecir Prioridad", variant="primary")
    resultado_html = gr.HTML()

    boton_predecir.click(
        fn=_predecir,
        inputs=[
            asunto_ticket,
            contenido_ticket,
            canal_ticket,
            categoria_problema,
            usuario_tipo_cuenta,
            usuario_antiguedad_dias,
        ],
        outputs=resultado_html,
    )


if __name__ == "__main__":
    demo.launch(theme=tema, css=CSS)
