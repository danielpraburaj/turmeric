import streamlit as st
import requests
from PIL import Image
import io

# Roboflow API Details
API_URL = "https://classify.roboflow.com/"
MODEL_ID = "test-jeatf"
VERSION = "1"
API_KEY = "baUupMb8dqcqk5qw0CUo"  # Replace with your Publishable API Key

# Streamlit App Title
st.title("🍎 Fruit Adulteration Detector")

# File uploader
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")

    # Run detection when the user clicks the button
    if st.button("Detect"):
        st.write("🔍 Sending image to Roboflow for detection...")

        # API Request
        url = f"{API_URL}{MODEL_ID}/{VERSION}?api_key={API_KEY}&confidence=0.1"
        response = requests.post(url, files={"file": image_bytes.getvalue()})

        # Check response
        if response.status_code == 200:
            result = response.json()
            st.write("✅ **Detection Results:**")
            if result.get("predictions"):
                for pred in result["predictions"]:
                    st.write(f"🔹 **{pred['class']}**: {round(pred['confidence'] * 100, 2)}% confidence")
            else:
                st.write("❌ No detections found. Try another image.")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
