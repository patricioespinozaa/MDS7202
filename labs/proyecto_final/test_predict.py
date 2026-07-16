import requests

URL = "http://127.0.0.1:8000"

print("LLamada exitosa:")
payload = {
    "asunto_ticket": "Transferencia fallida y dinero descontado",
    "contenido_ticket": (
        "Hola, intenté hacer una transferencia a otro banco y me descontaron la plata "
        "pero el destinatario dice que nunca le llegó. Necesito que revisen esto urgente "
        "porque es un monto importante."
        ),
        "canal_ticket":"Whatsapp",
        "categoria_problema":"Cuenta",
    }

# print input
print("Input:", payload)

response = requests.post(f"{URL}/predict", json=payload)
print("Status Code:", response.status_code)
if response.status_code == 200:
    print("Predicción de Nivel_Prioridad:", response.json())


print("\nLLamada no exitosa:")

payload_fail = {
    "asunto_ticket": "Prueba",
    "contenido_ticket": "Contenido de prueba",
    "canal_ticket": "Telegram",  
    "categoria_problema": "Cuenta",
}
print("Input:", payload_fail)
response_fail = requests.post(f"{URL}/predict", json=payload_fail)

print("Status Code:", response_fail.status_code)
if response_fail.status_code != 200:
    print("Error:", response_fail.json())