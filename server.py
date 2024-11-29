from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)
#     return jsonify({"message": "File uploaded successfully", "filepath": filepath})

@app.route('/modify', methods=['POST'])
def modify_file():
    data = request.get_json()
    filepath = data.get("filepath")
    modifications = data.get("modifications")  # Details of modifications

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        df = pd.read_excel(filepath)
        # Example modification: adding a new column
        df['NewColumn'] = 'Example Data'
        modified_filepath = filepath.replace('.xlsx', '_modified.xlsx')
        df.to_excel(modified_filepath, index=False)
        return jsonify({"message": "File modified successfully", "modified_filepath": modified_filepath})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

