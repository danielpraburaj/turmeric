import streamlit as st
import requests
from PIL import Image
import io

# Roboflow API Details
API_URL = "https://classify.roboflow.com/"
MODEL_ID = "test-jeatf"
VERSION = "1"
API_KEY = "baUupMb8dqcqk5qw0CUo"  # Replace with your Publishable API Key

# Hide Streamlit Branding (Header, Footer, and Menu)
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Streamlit App Title
st.title("Turmeric Adulteration - Testing")

# Option to either upload an image or take a picture
st.write("**Choose an option:**")
upload_option = st.radio("Select input method:", ("Upload Image", "Take a Picture"))

# Image Upload or Camera Input
if upload_option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
else:
    uploaded_file = st.camera_input("Take a picture")

if uploaded_file:
    # Open the image
    image = Image.open(uploaded_file)

    # Resize the image for display (e.g., 200x200 pixels)
    small_image = image.resize((200, 200))

    # Display the resized image
    st.image(small_image, caption="Selected Image", use_column_width=False)

    # Convert image to bytes for API request
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")

    # Run detection when the user clicks the button
    if st.button("Detect"):
        st.write("🔍 Detecting toxins...")

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
