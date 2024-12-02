from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import os

import base64

app = Flask(__name__)
CORS(app)

CSV_FILE_PATH = 'excel_contratos.csv'


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
def subir_archivo():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el archivo en la solicitud'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo no válido'}), 400
        
        file.save(CSV_FILE_PATH)
        
        return jsonify({'mensaje': 'Archivo subido exitosamente', 'nombre_archivo': file.filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# @app.route('/upload/excel', methods=['POST'])
# def subir_archivo():
#     try:
#         data = request.get_json()
#         if not data or 'file_name' not in data or 'file_data' not in data:
#             return jsonify({'error': 'Solicitud inválida, se requieren los campos file_name y file_data'}), 400

#         file_name = data['file_name']
#         file_data = data['file_data']

#         # Decodificar el contenido del archivo
#         file_bytes = base64.b64decode(file_data)

#         # Sanitizar el nombre del archivo para evitar problemas de seguridad
#         file_name = os.path.basename(file_name)

#         # Guardar el archivo en el directorio de uploads
#         file_path = CSV_FILE_PATH
#         with open(file_path, 'wb') as f:
#             f.write(file_bytes)

#         return jsonify({'mensaje': 'Archivo subido exitosamente', 'nombre_archivo': file_name}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5000
    app.run(host='0.0.0.0', port=5000)

