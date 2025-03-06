import os
import subprocess
from PIL import Image
import streamlit as st

def apply_filter(image, filter_type):
    """Ejecuta un script externo y devuelve todas las imágenes generadas en la carpeta correspondiente."""
    image.save("image.jpg")  # Guardar imagen temporalmente
    
    # Definir carpeta y script según el filtro seleccionado
    filter_mapping = {
        "Test Python": ("python", "unit_test.py"),
        "Test Numpy": ("numpy", "unit_test_numpy.py")
    }
    
    if filter_type not in filter_mapping:
        raise ValueError("Filtro no reconocido. Usa 'Test Python' o 'Test Numpy'.")

    folder, script = filter_mapping[filter_type]

    # Ejecutar el script correspondiente
    subprocess.run(["python", script], check=True)

    # Obtener todas las imágenes generadas en la carpeta
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        raise FileNotFoundError(f"No se generaron imágenes en la carpeta '{folder}'.")

    # Abrir todas las imágenes y devolverlas en una lista
    images = [Image.open(os.path.join(folder, img_file)) for img_file in image_files]
    
    return images

# ---- INTERFAZ EN STREAMLIT ----
st.title("Image Processing App - Testing Beta 3")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)
    
    filter_type = st.selectbox("Choose a filter", ["Test Python", "Test Numpy"])
    
    if st.button("Apply Filter"):
        try:
            result_images = apply_filter(image, filter_type)
            for img in result_images:
                st.image(img, caption="Processed Image", use_column_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
