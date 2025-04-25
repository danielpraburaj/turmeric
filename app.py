import streamlit as st
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient

# Roboflow Inference API Client
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="CpyMwjIoiSYVQP2aII6h"  # Use your actual API key
)

WORKSPACE_NAME = "turmeric-rlloj"
WORKFLOW_ID = "detect-and-classify"

# Hide Streamlit Branding
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# App Title
st.title("Turmeric - Testing")

# Upload or Capture Option
st.write("**Choose an option:**")
upload_option = st.radio("Select input method:", ("Upload Image", "Take a Picture"))

# Image Input
if upload_option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
else:
    uploaded_file = st.camera_input("Take a picture")

if uploaded_file:
    image = Image.open(uploaded_file)
    small_image = image.resize((200, 200))
    st.image(small_image, caption="Selected Image", use_column_width=False)

    # Save image to BytesIO
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    if st.button("Detect"):
        st.write("🔍 Running detection and classification...")

        # Run the workflow
        result = client.run_workflow(
            workspace_name=WORKSPACE_NAME,
            workflow_id=WORKFLOW_ID,
            images={"image": image_bytes},
            use_cache=True
        )

        # Display results
        if result and "results" in result:
            st.success("✅ Detection Completed")
            for res in result["results"]:
                if "predictions" in res:
                    for pred in res["predictions"]:
                        label = pred.get("class", "Unknown")
                        conf = round(pred.get("confidence", 0) * 100, 2)
                        st.write(f"🔹 **{label}**: {conf}% confidence")
                else:
                    st.write("❌ No objects detected.")
        else:
            st.error("❌ Error processing the image or no results returned.")
