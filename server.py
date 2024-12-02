from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permite solicitudes CORS desde cualquier origen

# Ruta al archivo CSV que deseas servir
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


if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5000
    app.run(host='0.0.0.0', port=5000)

