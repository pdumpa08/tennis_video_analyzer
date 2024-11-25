from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
from transform_video import process_video
import sys

print(sys.path)

app = Flask(__name__)

# Folder paths for uploading and serving static files
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static/processed_videos'

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Configure Flask to accept uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Limit to 50 MB

# Route for the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle video upload and processing
@app.route('/process-video', methods=['POST'])
def upload_and_process():
    if 'video' not in request.files:
        return jsonify({"success": False, "message": "No file part"})

    file = request.files['video']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})

    # Save the uploaded file temporarily
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Process the video
    processed_filename = process_video(input_path)

    video_url = f'static/outputs/output_video1.avi'
    return jsonify({"success": True, "video_url": video_url})

# Route for serving static files (processed videos)
@app.route('/static/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('static', filename)

# Main entry point for the application
if __name__ == "__main__":
    app.run(debug=True)
