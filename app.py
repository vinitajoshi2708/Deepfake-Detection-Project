import os
import numpy as np
import io  # <--- Yeh naya add kiya hai
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app)

# Model load karne ka sahi rasta
MODEL_PATH = 'saved_model/model.h5'

if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
else:
    print(f"Error: {MODEL_PATH} not found!")

@app.route('/')
def home():
    return "<h1 style='text-align:center; color:green;'>Deepfake Detector API is Running! ✅</h1>"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # --- ERROR FIX YAHAN HAI ---
    # File ko bytes mein convert karke load karna
    img_bytes = file.read()
    img = image.load_img(io.BytesIO(img_bytes), target_size=(128, 128))
    # ---------------------------

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)[0][0]
    
    is_real = True if prediction > 0.5 else False
    label = "REAL" if is_real else "FAKE"
    
    conf_value = prediction if is_real else (1 - prediction)
    confidence_pct = round(float(conf_value) * 100, 2)

    return jsonify({
        'is_real': is_real,
        'label': label,
        'confidence': str(confidence_pct)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)