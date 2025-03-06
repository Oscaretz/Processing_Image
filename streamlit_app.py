import streamlit as st
from PIL import Image
import numpy as np
import subprocess

def apply_filter(image, filter_type):
    image.save("temp_input.jpg")  # Guardar imagen temporalmente

    if filter_type == "Test Python":
        subprocess.run(["python", "unit_test_python.py", "temp_input.jpg", "temp_output.jpg"])
    elif filter_type == "Test Numpy":
        subprocess.run(["python", "unit_test_numpy.py", "temp_input.jpg", "temp_output.jpg"])
    
    return Image.open("temp_output.jpg")

st.title("Image Processing App - Testing beta")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)
    
    filter_type = st.selectbox("Choose a filter", ["Test Python", "Test Numpy"])
    
    if st.button("Apply Filter"):
        result_image = apply_filter(image, filter_type)
        st.image(result_image, caption="Processed Image", use_column_width=True)
