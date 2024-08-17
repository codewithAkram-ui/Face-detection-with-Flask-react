from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

# Load pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('C:/Users/91906/OneDrive/Desktop/python/flask/haarcascade_frontalface_default.xml')

# Ensure Haar Cascade is loaded successfully
assert not face_cascade.empty(), "Failed to load Haar Cascade XML file."

def detect_face(img_path):
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        print("Failed to load image")
        return False
    
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )

   
    return len(faces) > 0

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Ensure the uploads directory exists
        os.makedirs('uploads', exist_ok=True)
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        result = detect_face(file_path)
        print(f"Detection result: {result}")  # Log the detection result
        os.remove(file_path)
        return jsonify({"is_face": result})
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
