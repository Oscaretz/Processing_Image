import time
import pathlib
from process_image_python import *

def test_filters() -> None:
    
    """Unit test to run all filters from one image input"""

    # Input/output paths
    input_path = str(pathlib.Path().resolve()) + "/image.jpeg"
    output_sobel = "python/output_sobel.jpg"
    output_gaussian = "python/output_gaussian.jpg"
    output_noise_reduction = "python/output_noise_reduction.jpg"
    
    # Read the input image
    print("Reading image...")
    image = read_image(input_path)
    
    # Test Sobel filter
    print("\nTesting Sobel filter...")
    start_time = time.time()
    sobel_image = apply_sobel(image)
    sobel_time = time.time() - start_time
    save_image(sobel_image, output_sobel)
    print(f"Sobel filter processing time: {sobel_time:.4f} seconds")
    
    # Test Gaussian filter
    print("\nTesting Gaussian filter...")
    start_time = time.time()
    kernel = create_gaussian_kernel(5, sigma=1)  # 5x5 kernel
    gaussian_image = apply_gaussian(image, kernel)
    gaussian_time = time.time() - start_time
    save_image(gaussian_image, output_gaussian)
    print(f"Gaussian filter processing time: {gaussian_time:.4f} seconds")


    # Test median noise-reduction filter
    print("\nTesting Median noise-reduction filter...")
    start_time = time.time()
    noise_reduction_image = apply_median_filter(image, kernel)
    noise_reduction_time = time.time() - start_time
    save_image(noise_reduction_image, output_noise_reduction)
    print(f"Median noise-reduction filter processing time: {noise_reduction_time:.4f} seconds")
    
    # Print summary
    print("\nSummary:")
    print(f"{'Filter Type':<20} {'Processing Time':>15}")
    print("-" * 35)
    print(f"{'Sobel':<20} {sobel_time:>15.4f}s")
    print(f"{'Gaussian':<20} {gaussian_time:>15.4f}s")  
    print(f"{'Median noise-reduction':<20} {noise_reduction_time:>13.4f}s")
    print(f"{'Total':<20} {(sobel_time + gaussian_time + noise_reduction_time):>15.4f}s")

if __name__ == "__main__":
    test_filters()
