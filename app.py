from flask import Flask, request, jsonify
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

# Esta es la ruta que va a recibir el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()  # Recibimos los datos en formato JSON
        print('Datos recibidos:', data)

        # Aquí puedes procesar los datos o guardarlos en una base de datos
        # Por ejemplo, enviar un correo o almacenar la información

        # Devolver una respuesta para confirmar que el webhook se recibió correctamente
        return jsonify({'message': 'Webhook recibido correctamente'}), 200

    except Exception as e:
        print('Error al procesar el webhook:', e)
        return jsonify({'message': 'Error al procesar el webhook'}), 500

# Iniciar el servidor en el puerto 5000
if __name__ == '__main__':
    app.run(debug=True, port=80)
