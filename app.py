from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import io
from PIL import Image

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("model.h5")

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to match model input
    image = np.array(image) / 255.0   # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    image = preprocess_image(image)

    prediction = model.predict(image)[0]
    result = "Leaded" if prediction[0] > prediction[1] else "Non-Leaded"

    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
