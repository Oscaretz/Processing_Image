import time
import pathlib
import csv
from process_image_python import *

def test_filters() -> None:
    """Unit test to run all filters from one image input and store the results in a CSV"""

    # Definir rutas de entrada y salida
    input_path = str(pathlib.Path().resolve()) + "/image.jpg"
    output_sobel = "python_dir/Sobel.jpg"
    output_gaussian = "python_dir/Gaussian.jpg"
    output_noise_reduction = "python_dir/Noise_reduction.jpg"

    # Definir el nombre del archivo CSV
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

        # Leer la imagen
        print("Reading image for python...")
        image = read_image(input_path)

        # Aplicar filtros y medir tiempo
        filters = [
            ("Sobel", apply_sobel, output_sobel),
            ("Gaussian", lambda img: apply_gaussian(img, create_gaussian_kernel(9, sigma=3)), output_gaussian),
            ("Median Noise-reduction", lambda img: apply_median_filter(img, (9, 9)), output_noise_reduction)

        ]



        for filter_name, filter_func, output_path in filters:
            print(f"\nTesting {filter_name} filter...")
            start_time = time.time()
            filtered_image = filter_func(image)
            elapsed_time = time.time() - start_time
            save_image(filtered_image, output_path)
            print(f"{filter_name} filter processing time: {elapsed_time:.4f} seconds")
            
            # Guardar en CSV
            writer.writerow({'Filter Type': filter_name, 'Implementation': 'Python', 'Processing Time (seconds)': elapsed_time})


    # Mostrar resumen
    print("\nSummary of python:")
    print(f"{'Filter Type':<25} {'Processing Time':>15}")
    print("-" * 40)
    for row in filters:
        print(f"{row[0]:<25} {elapsed_time:>15.4f}s")
    print("Python finished")

if __name__ == "__main__":
    test_filters()
