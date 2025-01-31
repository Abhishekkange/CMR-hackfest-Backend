import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from agents import imageDecoderAgent, factCheckingAgent
from jsonparser import custom_json_parser



app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a simple route
@app.route('/checknewsmobile', methods=['POST'])
def home():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        response = imageDecoderAgent.run(file_path)
        response2 = factCheckingAgent.run(response.content)
        # Parsing the response for json output
        finalRes = custom_json_parser(response2)
        return finalRes


    return jsonify({"error": "Invalid file type"}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)