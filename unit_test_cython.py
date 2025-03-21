import time
import numpy as np
import pathlib
import csv
from process_image_cython import (
    read_image,
    save_image,
    create_gaussian_kernel,
    apply_filter,
    apply_sobel,
    apply_median_filter
)


def test_filters():
    """Unit test to run all filters from one image input and store the results in a CSV"""

    # Input/output paths
    input_path = str(pathlib.Path().resolve()) + "/image.jpg"
    output_sobel = "cython/Sobel.jpg"
    output_gaussian = "cython/Gaussian.jpg"
    output_noise_reduction = "cython/Noise_reduction.jpg"

    # Definir la ruta y archivo CSV
    csv_dir = pathlib.Path("metrics")
    csv_file = csv_dir / "values.csv"

    # Crear carpeta 'metrics' si no existe
    csv_dir.mkdir(parents=True, exist_ok=True)

    # Definir nombres de columnas del CSV
    fieldnames = ['Filter Type', 'Implementation', 'Processing Time (seconds)']

    # Verificar si el archivo ya existe y si está vacío
    file_exists = csv_file.exists()
    file_empty = not file_exists or csv_file.stat().st_size == 0  # True si el archivo no existe o está vacío

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Escribir encabezados solo si el archivo es nuevo o está vacío
        if file_empty:
            writer.writeheader()

        # Read the input image
        print("Reading image...")
        image = read_image(input_path)

        # Aplicar filtros y medir tiempo
        filters = [
            ("Sobel", apply_sobel, output_sobel),
            ("Gaussian", lambda img: apply_filter(img, create_gaussian_kernel(9, sigma=3)), output_gaussian),
            ("Median Noise-reduction", lambda img: apply_median_filter(img, 3), output_noise_reduction)
        ]

        for filter_name, filter_func, output_path in filters:
            print(f"\nTesting {filter_name} filter...")
            start_time = time.time()
            filtered_image = filter_func(image)
            elapsed_time = time.time() - start_time
            save_image(filtered_image, output_path)
            print(f"{filter_name} filter processing time: {elapsed_time:.4f} seconds")
            
            # Guardar en CSV
            writer.writerow({'Filter Type': filter_name, 'Implementation': 'Cython', 'Processing Time (seconds)': elapsed_time})

    # Mostrar resumen
    print("\nSummary:")
    print(f"{'Filter Type':<20} {'Processing Time':>15}")
    print("-" * 35)
    for filter_name, _, _ in filters:
        print(f"{filter_name:<20} {elapsed_time:>15.4f}s")
    print("Cython finished")

if __name__ == "__main__":
    test_filters()
