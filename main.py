import openai
from flask import Flask, request, jsonify

import os
openai.api_key = os.getenv("OPENAI_API_KEY")
print("Clave cargada desde variable:", openai.api_key)

# Aquí debes colocar tu clave API de OpenAI

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()
        print("Datos recibidos:", data)

        if 'mensaje' not in data:
            return jsonify({'error': 'No se encontró el campo "mensaje" en los datos'}), 400

        mensaje_usuario = data['mensaje']

        # Enviar el mensaje a OpenAI y obtener la respuesta
        respuesta_openai = obtener_respuesta_openai(mensaje_usuario)

        # Devolver la respuesta generada por OpenAI
        return jsonify({'mensaje': respuesta_openai}), 200

    except Exception as e:
        # Capturamos cualquier error que ocurra durante el procesamiento del webhook
        print("Error al procesar el webhook:", e)
        return jsonify({'error': 'Error al procesar el webhook', 'details': str(e)}), 500


# Función para obtener la respuesta de OpenAI
def obtener_respuesta_openai(mensaje):
    try:
        # Solicitar la respuesta de OpenAI utilizando el endpoint chat completions
        print(f"Enviando solicitud a OpenAI con el mensaje: {mensaje}")

        # Usamos el endpoint chat completions para modelos como gpt-3.5-turbo y gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa el modelo adecuado (gpt-3.5-turbo o gpt-4)
            messages=[{"role": "user", "content": mensaje}],  # Usamos el formato de mensajes para el chat
            max_tokens=150  # Limita el número de tokens en la respuesta
        )

        print(f"Respuesta de OpenAI: {response}")
        return response['choices'][0]['message']['content'].strip()  # Obtener la respuesta del modelo

    except Exception as e:
        # Capturamos cualquier error general
        print(f"Error general al conectar con OpenAI: {e}")
        return f"Lo siento, ocurrió un error al procesar tu mensaje: {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
