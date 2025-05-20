from flask import Flask, render_template, request, jsonify, send_from_directory, after_this_request
import os
import cv2
import numpy as np
import pandas as pd
import base64
import time
import uuid
from werkzeug.utils import secure_filename

from parking_detection import (
    manual_count_based_on_image,
    export_results_to_csv
)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    @after_this_request
    def add_no_cache(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
        
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            unique_id = str(uuid.uuid4())[:8]
            original_filename = secure_filename(file.filename)
            filename = f"{unique_id}_{original_filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            image = cv2.imread(file_path)
            if image is None:
                return jsonify({'error': 'Could not read the image. Please try another image.'}), 400

            h, w = image.shape[:2]
            if h < 100 or w < 100:
                return jsonify({'error': 'Image is too small. Please upload a larger image.'}), 400
        
            results = manual_count_based_on_image(image)
            if 'error' in results:
                return jsonify({
                    'error': results['error'],
                    'is_parking_lot': False,
                    'message': 'The uploaded image does not appear to be a parking lot. Please upload a clear image of a parking lot.'
                }), 400
            csv_filename = os.path.splitext(filename)[0] + '_results.csv'
            csv_path = os.path.join(app.config['RESULTS_FOLDER'], csv_filename)
            df = export_results_to_csv(
                results['Total Number of Slots'],
                results['Occupied Slots'],
                results['Available Slots'],
                filename=csv_path
            )
            response_data = {
                'success': True,
                'total_slots': results['Total Number of Slots'],
                'occupied_slots': results['Occupied Slots'],
                'available_slots': results['Available Slots'],
                'csv_file': csv_filename,
                'image_info': {
                    'width': w,
                    'height': h,
                    'size_kb': os.path.getsize(file_path) // 1024
                }
            }
            if app.debug and 'Analysis' in results:
                response_data['analysis'] = results['Analysis']
            
            return jsonify(response_data)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f"Error processing the image: {str(e)}"}), 500
    
    return jsonify({'error': 'Failed to process the file'}), 500
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)