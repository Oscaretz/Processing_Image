import time
import pathlib
import csv
import os
from process_image_numpy import *

def test_filters() -> None:
    """Unit test to run all filters from one image input and store the results in a CSV"""

    # Input/output paths
    input_path = str(pathlib.Path().resolve()) + "/image.jpg"
    output_sobel = "numpy_dir/Sobel.jpg"
    output_gaussian = "numpy_dir/Gaussian.jpg"
    output_noise_reduction = "numpy_dir/Noise_reduction.jpg"
    
    # Prepare CSV for writing results
    csv_file = 'metrics/values.csv'
    fieldnames = ['Filter Type', 'Implementation', 'Processing Time (seconds)']
    
    # Check if file exists and is not empty
    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write headers only if the file is new or empty
        if not file_exists:
            writer.writeheader()

        # Read the input image
        print("Reading image for numpy...")
        image = read_image(input_path)
        
        # Test Sobel filter
        print("\nTesting Sobel filter...")
        start_time = time.time()
        sobel_image = apply_sobel(image)  # Implementación en Numpy
        sobel_time = time.time() - start_time
        save_image(sobel_image, output_sobel)
        print(f"Sobel filter processing time: {sobel_time:.4f} seconds")
        writer.writerow({'Filter Type': 'Sobel', 'Implementation': 'Numpy', 'Processing Time (seconds)': sobel_time})
        
        # Test Gaussian filter
        print("\nTesting Gaussian filter...")
        start_time = time.time()
        kernel = create_gaussian_kernel(9, sigma=3)  # nxn kernel
        gaussian_image = apply_filter(image, kernel)  # Implementación en Numpy
        gaussian_time = time.time() - start_time
        save_image(gaussian_image, output_gaussian)
        print(f"Gaussian filter processing time: {gaussian_time:.4f} seconds")
        writer.writerow({'Filter Type': 'Gaussian', 'Implementation': 'Numpy', 'Processing Time (seconds)': gaussian_time})

        # Test median noise-reduction filter
        print("\nTesting Median noise-reduction filter...")
        start_time = time.time()
        noise_reduction_image = apply_median_filter(image, 3)  # 3x3 median filter
        noise_reduction_time = time.time() - start_time
        save_image(noise_reduction_image, output_noise_reduction)
        print(f"Median noise-reduction filter processing time: {noise_reduction_time:.4f} seconds")
        writer.writerow({'Filter Type': 'Median Noise-reduction', 'Implementation': 'Numpy', 'Processing Time (seconds)': noise_reduction_time})
        

    
    # Print summary
    print("\nSummary of numpy:")
    print(f"{'Filter Type':<20} {'Processing Time':>15}")
    print("-" * 35)
    print(f"{'Sobel':<20} {sobel_time:>15.4f}s")
    print(f"{'Gaussian':<20} {gaussian_time:>15.4f}s")  
    print(f"{'Median noise-reduction':<20} {noise_reduction_time:>13.4f}s")
    print("Finish")

if __name__ == "__main__":
    test_filters()
