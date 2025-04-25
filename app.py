import streamlit as st
import requests
from PIL import Image
import io

# Roboflow API Details
API_URL = "https://classify.roboflow.com/"
MODEL_ID = "t-2-a32a3"
VERSION = "6"
API_KEY = "CpyMwjIoiSYVQP2aII6h" 

# Hide Streamlit Branding (Header, Footer, and Menu)
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# App Title
st.title("🌿 Turmeric Adulteration - Testing")

# Choose Input Method
st.write("**Choose an option:**")
upload_option = st.radio("Select input method:", ("Upload Image", "Take a Picture"))

# Handle image upload or capture
if upload_option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
else:
    uploaded_file = st.camera_input("Take a picture")

if uploaded_file:
    # Open the image
    image = Image.open(uploaded_file)

    # Resize for display
    small_image = image.resize((200, 200))
    st.image(small_image, caption="Selected Image", use_container_width=False)

    # Convert to bytes for API
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")

    if st.button("Detect"):
        st.write("🔍 Detecting...")

        # Roboflow API call
        url = f"{API_URL}{MODEL_ID}/{VERSION}?api_key={API_KEY}&confidence=0.1"
        response = requests.post(url, files={"file": image_bytes.getvalue()})

        if response.status_code == 200:
            result = response.json()
            preds = result.get("predictions", [])

            # Use the most confident prediction only
            top_pred = max(preds, key=lambda p: p['confidence']) if preds else None

            if top_pred:
                label = top_pred['class'].lower()

                if "lead" in label:
                    st.error("❌ Contaminated with lead.")
                else:
                    st.success("✅ Appears clean.")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
