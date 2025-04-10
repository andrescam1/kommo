import openai
from flask import Flask, request, jsonify

import os
openai.api_key = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID=os.environ.get("ASSISTANT_ID")
# openai.api_key = os.getenv("OPENAI_API_KEY")
print("Clave cargada desde variable:", openai.api_key)
print("Variables de entorno disponibles:",ASSISTANT_ID)

# Aquí debes colocar tu clave API de OpenAI

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        if 'mensaje' not in data:
            return jsonify({'error': 'No se encontró el campo "mensaje" en los datos'}), 400

        mensaje_usuario = data['mensaje']

        respuesta = obtener_respuesta_openai(mensaje_usuario)

        return jsonify({'mensaje': respuesta}), 200

    except Exception as e:
        print("Error al procesar el webhook:", e)
        return jsonify({'error': 'Error al procesar el webhook', 'details': str(e)}), 500


def obtener_respuesta_openai(mensaje):
    try:
        # 1. Crear un nuevo hilo
        thread = openai.beta.threads.create()

        # 2. Enviar el mensaje del usuario al hilo
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=mensaje
        )

        # 3. Iniciar la ejecución del asistente
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4. Esperar a que el asistente termine
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                return "El Assistant falló al procesar el mensaje."
            time.sleep(1)

        # 5. Obtener la respuesta del asistente
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value.strip()

        return "No se encontró respuesta del Assistant."

    except Exception as e:
        print(f"Error al usar el Assistant: {e}")
        return f"Ocurrió un error al procesar tu mensaje: {e}"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
