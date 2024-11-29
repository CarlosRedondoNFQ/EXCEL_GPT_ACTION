from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

PATH = "./Excel_Contratos.xlsx"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    try:
        file.save(PATH)
        return jsonify({"message": "File uploaded successfully", "filepath": PATH})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/excel', methods=['GET'])
def download_file():
    if not os.path.exists(PATH):
        return jsonify({"error": "File not found"}), 404
    try:
        return send_file(PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
