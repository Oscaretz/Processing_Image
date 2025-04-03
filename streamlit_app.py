import os
import subprocess
import pandas as pd
import time, math
from PIL import Image
import streamlit as st
from streamlit_echarts import st_echarts
import sys


os.system("pip install --no-cache-dir Pillow")


def check_installed(package):
    try:
        subprocess.run(["pip", "show", package], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

if not check_installed("Pillow"):
    print("⚠️ Pillow NO está instalado en el entorno de Streamlit Cloud.")

import PIL  # Esto fallará si no está instalado
print("✅ Pillow está instalado correctamente.")

def apply_filter(image, script_name):
    """Ejecuta un script externo y mide su tiempo de ejecución."""
    
    # Guardar la imagen temporalmente
    image.save("image.jpg")

    # Medir el tiempo de ejecución
    start_time = time.time()
    
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al ejecutar {script_name}: {e}")

    return time.time() - start_time  # Retorna el tiempo de ejecución

def read_metrics_csv(csv_path):
    """Lee el CSV de métricas y devuelve un DataFrame formateado correctamente."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo de métricas '{csv_path}'.")
    
    df = pd.read_csv(csv_path)

    # Renombrar columnas para facilitar el manejo
    df.rename(columns={"Filter Type": "Filter", "Implementation": "Method", "Processing Time (seconds)": "Time"}, inplace=True)

    # Transformar la tabla para que tenga columnas separadas para Python y Numpy
    metrics_pivot = df.pivot(index="Filter", columns="Method", values="Time").reset_index()

    return metrics_pivot  # Devuelve el DataFrame con la estructura correcta

# ---- INTERFAZ EN STREAMLIT ----
st.title("High Performance Computing")
'''
Browse image processing performance metrics using Python, NumPy, and Cython. This project applies various filters—such as Sobel, Gaussian, and noise reduction—to analyze execution times and visualize the results. By comparing these implementations, we assess their efficiency and speed. Upload an image, apply filters, and explore performance insights interactively! 🚀
'''
st.header("Image Processing", divider='gray')

# Opciones: subir imagen o tomar foto
option = st.radio("Choose input method:", ("Upload an image", "Take a photo"))

image = None

if option == "Upload an image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)

elif option == "Take a photo":
    camera_file = st.camera_input("Take a photo")
    if camera_file:
        image = Image.open(camera_file)

if image:
    st.image(image, caption="Original Image", use_container_width=True)  

    if st.button("Apply Filter"):
        try:
            metrics_file = "metrics/values.csv"

            # Borrar archivo de métricas si existe
            if os.path.exists(metrics_file):
                os.remove(metrics_file)

            # Aplicar filtros con Python y Numpy
            time_python = apply_filter(image, "unit_test.py")
            time_numpy = apply_filter(image, "unit_test_numpy.py")
            time_cython = apply_filter(image, "unit_test_cython.py")

            # Leer métricas desde el CSV
            metrics_df = read_metrics_csv(metrics_file)

            # Verificar que las columnas sean correctas
            if "Python" not in metrics_df.columns or "Numpy" not in metrics_df.columns:
                st.error(f"Error: No se encontraron las columnas 'Python' o 'Numpy'. Columnas actuales: {list(metrics_df.columns)}")
            else:
               # ---- PERFORMANCE ----
                # Read execution time metrics
                metrics_df = read_metrics_csv("metrics/values.csv")

                st.header('Speedup Analysis', divider='gray')

                # Crear columnas para mostrar las métricas
                cols = st.columns(3)

                for i, filter_name in enumerate(metrics_df["Filter"]):
                    col = cols[i % len(cols)]  # Distribuir en columnas

                    with col:
                        python_time = metrics_df[metrics_df["Filter"] == filter_name]["Python"].iat[0]
                        numpy_time = metrics_df[metrics_df["Filter"] == filter_name]["Numpy"].iat[0]
                        cython_time = metrics_df[metrics_df["Filter"] == filter_name]["Cython"].iat[0]

                        # Calcular Speedup (manejando división por cero)
                        speedup_numpy = python_time / numpy_time if numpy_time > 0 else float('inf')
                        speedup_cython = python_time / cython_time if cython_time > 0 else float('inf')

                        # Determinar color verde cuando NumPy o Cython son más rápidos
                        delta_color_numpy = "normal" if speedup_numpy > 1 else "inverse"
                        delta_color_cython = "normal" if speedup_cython > 1 else "inverse"

                        # Mostrar ejecución de Python
                        st.metric(label=f'Python ({filter_name})', value=f'{python_time:.4f}s')

                        # Mostrar ejecución de NumPy con Speedup en verde
                        st.metric(
                            label=f'NumPy ({filter_name})',
                            value=f'{numpy_time:.4f}s',
                            delta=f'{speedup_numpy:,.2f}x',
                            delta_color=delta_color_numpy
                        )

                        # Mostrar ejecución de Cython con Speedup en verde
                        st.metric(
                            label=f'Cython ({filter_name})',
                            value=f'{cython_time:.4f}s',
                            delta=f'{speedup_cython:,.2f}x',
                            delta_color=delta_color_cython
                        )

                # ---- GRAFICAR TIEMPOS ----
                st.header("Execution Time Comparison", divider='gray')

                option = {
                    "tooltip": {"trigger": "axis"},
                    "legend": {"data": ["Python", "Numpy", "Cython"]},
                    "xAxis": {
                        "type": "category",
                        "data": metrics_df["Filter"].tolist(),  # Nombres de los filtros
                    },
                    "yAxis": {"type": "value", "name": "Time (seconds)"},
                    "series": [
                        {
                            "name": "Python",
                            "data": metrics_df["Python"].tolist(),  # Tiempos de Python
                            "type": "bar",
                            "color": "red",
                        },
                        {
                            "name": "Numpy",
                            "data": metrics_df["Numpy"].tolist(),  # Tiempos de Numpy
                            "type": "bar",
                            "color": "blue",
                        },
                        {
                            "name": "Cython",
                            "data": metrics_df["Cython"].tolist(),  # Tiempos de Cython
                            "type": "bar",
                            "color": "green",
                        }
                    ],
                }

                # Plotting
                st_echarts(options=option, height="400px")

                # ---- GRAFICAR IMAGENES EN TABLA ----
                print('Printing the image results...')
                # Directorios donde están guardadas las imágenes
                python_dir = "python"
                numpy_dir = "numpy"
                cython_dir = "cython"

                # Lista de filtros utilizados
                filters = ["Sobel", "Gaussian", "Noise_reduction"]

                # Mostrar título
                st.write("### Filter Results")

                # Crear tabla con imágenes en Streamlit
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**Filter**")

                with col2:
                    st.write("**Python**")

                with col3:
                    st.write("**Numpy**")

                with col4:
                    st.write("**Cython**")

                for filter_name in filters:
                    python_img = os.path.join(python_dir, f"{filter_name}.jpg")
                    numpy_img = os.path.join(numpy_dir, f"{filter_name}.jpg")
                    cython_img = os.path.join(cython_dir, f"{filter_name}.jpg")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.write(f"**{filter_name}**")

                    with col2:
                        if os.path.exists(python_img):
                            st.image(python_img, caption="Python", use_container_width=True)
                        else:
                            st.write("❌ No Image")

                    with col3:
                        if os.path.exists(numpy_img):
                            st.image(numpy_img, caption="Numpy", use_container_width=True)
                        else:
                            st.write("❌ No Image")

                    with col4:
                        if os.path.exists(cython_img):
                            st.image(cython_img, caption="Cython", use_container_width=True)
                        else:
                            st.write("❌ No Image")


                

                


        except Exception as e:
            st.error(f"Error: {e}")



# ---- FOOTER ----
st.markdown(
    """
    ---
    **Developed by Oscar Martinez Estevez, Braulio Perez Tamayo, Moises Carrillo Alonzo and David Hernandez Pantoja.**  
    GitHub: [Oscaretz/Processing_Image](https://github.com/Oscaretz/Processing_Image)  
    """, 
    unsafe_allow_html=True
)
