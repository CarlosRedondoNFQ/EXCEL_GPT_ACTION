from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

PATH = "./Excel_Contratos.xlsx"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    # filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(PATH)
    return jsonify({"message": "File uploaded successfully", "filepath": PATH})


@app.route('/download/excel', methods=['GET'])
def download_file():
    # filepath = os.path.join(UPLOAD_FOLDER, filename)
    filepath = PATH
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


