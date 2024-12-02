from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import os
import logging

import base64

app = Flask(__name__)
CORS(app)

CSV_FILE_PATH = 'excel_contratos.csv'

# Setup logging
logging.basicConfig(level=logging.DEBUG)


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error("Unhandled Exception", exc_info=e)
    return {"error": str(e)}, 500


@app.route('/download/excel', methods=['GET'])
def descargar_datos():
    try:
        # Verifica si el archivo existe
        if not os.path.exists(CSV_FILE_PATH):
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        # Envía el archivo CSV como respuesta
        return send_file(
            CSV_FILE_PATH,
            mimetype='text/csv',
            as_attachment=True,
            download_name='excel_contratos.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/upload/excel', methods=['POST'])
def subir_archivo_como_texto():
    print("Request Content-Type:", request.content_type)
    print("Request files:", request.files)
    print("Request form:", request.form)

    try:
        if request.content_type != 'application/json':
            return jsonify({'error': 'El tipo de contenido debe ser application/json'}), 400

        # Leer el contenido JSON
        data = request.get_json()
        if 'file_name' not in data or 'file_content' not in data:
            return jsonify({'error': 'JSON inválido. Se requieren los campos file_name y file_content'}), 400

        file_name = data['file_name']
        file_content = data['file_content']

        # Guardar el contenido del archivo como CSV
        with open(CSV_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(file_content)

        return jsonify({'mensaje': 'Archivo subido exitosamente', 'nombre_archivo': file_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5000
    app.run(host='0.0.0.0', port=5000)

