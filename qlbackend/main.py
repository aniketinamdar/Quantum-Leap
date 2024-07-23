from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import requests
from tensorflow.keras.models import load_model
import os

MODEL_URL = 'https://qleapmodel.s3.amazonaws.com/model_100.h5'
MODEL_DIR = os.path.join(os.getcwd(), 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model_100.h5')

os.makedirs(MODEL_DIR, exist_ok=True)

# Check if the model file already exists
if not os.path.exists(MODEL_PATH):
    response = requests.get(MODEL_URL)
    if response.status_code == 200:
        print('Downloading the model from S3')
        with open(MODEL_PATH, 'wb') as f:    
            f.write(response.content)
    else:
        raise ValueError('Failed to download the model from S3')
else:
    print('Model already exists. Skipping download.')

# Load the model
model = load_model(MODEL_PATH)
if model is None:
    raise ValueError('Model not found')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

def load_and_preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((256, 256))
    img_array = np.array(img)
    img_array = img_array / 255.0
    return img_array

def predict_image_class(img_array):
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    class_probabilities = predictions[0]
    return predicted_class, class_probabilities

@app.route('/')
def main():
    return "Flask app is running"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        img_array = load_and_preprocess_image(img)

        predicted_class, class_probabilities = predict_image_class(img_array)
        if int(predicted_class) == 0:
            class_ = 'Bordered'
        elif int(predicted_class) == 1:
            class_ = 'Borderless'
        elif int(predicted_class) == 2:
            class_ = 'Row Bordered'
        else:
            class_ = 'Unknown'
        return jsonify({
            'predicted_class': class_,
            'class_probabilities': class_probabilities.tolist()
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
