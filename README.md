# 🖼️ Image Processing with Python, NumPy & Cython

Welcome to a fast and interactive web app for image preprocessing using filters like Sobel, Gaussian, and Median! Built with Python, NumPy, Pillow, and accelerated with Cython. Deployed live using **Streamlit Cloud**.

## 🎯 Project Objective

This project aims to showcase the potential of **High Performance Computing (HPC)** in image processing through a comparative study of three implementations: **pure Python**, **NumPy**, and **Cython**. Each version applies the same filters and reports the processing time, enabling a visual and performance-based evaluation of optimization techniques.

Through this demonstration, we highlight how computing performance improves by moving from interpreted code to compiled extensions — a key idea behind HPC.

---

## 🚀 Features

- 🌀 Apply **Sobel**, **Gaussian**, and **Median** filters to images
- 📈 Visualize and compare performance across Python, NumPy, and Cython
- 📷 Upload your own images to test
- ☁️ Fully deployable on **Streamlit Cloud**
- ⚡ Performance boosted using **Cython** extensions

---

## 🛠️ Technologies Used

- `Python` 🐍
- `NumPy` 📦
- `Pillow` 🖼️
- `Cython` ⚡
- `Streamlit` 🌐
- `Matplotlib` 📊
- `SciPy` 🔬
- `Setuptools` 🛠️
- `Pathlib` 🧱

---

## 📸 Example

![App Screenshot](https://github.com/Oscaretz/Processing_Image/blob/main/screen_shoots/testing.gif)


---

## 📦 Installation

To run the app locally:

```bash
git clone https://github.com/Oscaretz/Processing_Image
cd processing_image
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚡ Cython Acceleration

This project supports **Cython** to accelerate heavy operations. To compile Cython modules:

1. Add your `.pyx` file (e.g., `process_image_cython.pyx`)
2. Create or update `setup.py`:

```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("process_image_cython.pyx")
)
```

3. Compile it:

```bash
python setup.py build_ext --inplace
```

---

## 🧪 Running Tests

To compare performance:

```bash
python unit_test_python.py
python unit_test_numpy.py
python unit_test_cython.py
```

---

## 🌍 Deployment

This app is already deployed on [**Streamlit Cloud**](https://imageprocessing-python-numpy-cython.streamlit.app/)! 🔗 

You can also deploy your own fork by pushing it to your GitHub and connecting it to Streamlit Cloud.

---

## ✨ Credits

Created by Oscar Martinez Estevez  
[GitHub ](https://github.com/Oscaretz)

---

