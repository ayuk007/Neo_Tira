import streamlit as st
from PIL import Image
import requests
import base64
import io
import json
from io import BytesIO

# Function to download image from URL
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Lambda API endpoint
API_ENDPOINT = "https://o6kuyvrcx5.execute-api.ap-south-1.amazonaws.com/initial/"

st.title("Image Processing App")

# Sidebar selection between camera and gallery
option = st.sidebar.selectbox("Select Image Source", ("Camera", "Gallery"))

if option == "Camera":
    # Capture image from camera
    uploaded_file = st.file_uploader("Capture Image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
elif option == "Gallery":
    # Upload image from gallery
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    # Display uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Send image to Lambda API
    data = img_str
    response = requests.post(API_ENDPOINT, json=data)

    # Display response from Lambda API
    if response.status_code == 200:
        result = response.json()
        result = json.loads(result["body"])
        img = download_image(result["Plotted Image URL"])
        st.write("Response from Lambda API:")
        st.image(img, caption="Downloaded Image", use_column_width=True)
        # Button to show image URL
        if st.button("Show Image URL"):
            st.write("Image URL:", result["Plotted Image URL"])

    else:
        st.error("Error: Failed to process the image. Please try again.")