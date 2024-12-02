from flask import Flask, request, jsonify, send_file
import os
import uuid
import datetime

app = Flask(__name__)

PATH = "./excel_contratos.csv"

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


# @app.route('/download/excel', methods=['GET'])
# def download_file():
#     if not os.path.exists(PATH):
#         return jsonify({"error": "File not found"}), 404
#     try:
#         return send_file(PATH, as_attachment=True)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/download/excel', methods=['GET'])
def download_file():
    if not os.path.exists(PATH):
        return jsonify({"error": "File not found"}), 404

    # Generate OpenAI-compatible file response metadata
    file_metadata = {
        "id": str(uuid.uuid4()),  # Unique identifier
        "object": "file",
        "bytes": os.path.getsize(PATH),
        "created_at": int(datetime.datetime.utcnow().timestamp()),
        "filename": os.path.basename(PATH),
        "purpose": "fine-tune"  # Adjust as needed (e.g., "answers", "fine-tune")
    }

    try:
        # Include the file metadata in the response headers
        response = send_file(PATH, as_attachment=True)
        response.headers['Content-Type'] = 'application/json'
        response.headers['X-OpenAI-File-Metadata'] = jsonify(file_metadata).get_data(as_text=True)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)