# Geospectral
## Overview
GeoSpectral is a high-performance multispectral image augmentation library designed for efficient geospatial data processing.

## Features
- **Raster Clipping**: Extract regions from large GeoTIFF files using shapefile boundaries
- **Multithreaded Support**: Choose between threaded and non-threaded operations
- **Performance Optimized**: 
    - Non-threaded clipping: ~7 seconds
    - Multithreaded clipping: ~2 seconds (4x faster)
- **Automatic Worker Detection**: Intelligent worker allocation based on system resources, or manual configuration

## Getting Started



**Import Packages**
```python
# Import Packages
from augmentation import clip_raster_threaded,clip_raster_serial
shape="data.shp"
tiff="data.tif"

)
```





**Non-threaded clipping:**
```python
# Basic usage example
clip_raster_serial(
    shapefile_path=shape,
    tiff_file=tiff,
    output_dir="tiles",

)
```


**Multithreaded clipping:**
```python
# Basic usage example
clip_raster_threaded(
    shapefile_path=shape,
    tiff_file=tiff,
    output_dir="tiles",

)

## Load filepaths after clipping

```python
filepath,filename=files_load("tiles")
print(filename)
```
This block of code will help to load all the absolute filepaths. It returns a tuple file location and file path.


## Applying Augmentations

```python
geometric_augmentations(
    image_path=filepath[0],
    aug_type=[],
    apply_all=True,
    noise=0.05,
    patchmix=True
)
```
This function  provides a lot of features ranging from just simple geometric augmentation to a bit advanced features like adding gaussian noise ,applying patchmix .  


**Geometric Augmentations**

This applies selected image transformations using NumPy:

* `H` → Horizontal flip
* `V` → Vertical flip
* `R` → Rotate 90°
* `R2` → Rotate 180°
* `R3` → Rotate 270°

You can pass specific augmentations in a list using `aug_type` (e.g., `["H", "R"]`) and set `apply_all=False` to apply only those operations.

Set `apply_all=True` to apply all augmentations.


---

**Gaussian Noise Augmentation**

You can add Gaussian noise to the image by simply passing a noise value (e.g., `noise=0.05`) when calling `geometric_augmentations`.

Example:

```python
geometric_augmentations(
    image_path=filepath[0],
    aug_type=[],
    apply_all=True,
    noise=0.05,
    patchmix=True
)
```

### How it works:

* The GeoTIFF bands are optionally normalized to the range `[0, 1]`
* Random Gaussian noise is generated using the provided `noise` value as the standard deviation
* Noise is added to each pixel across all bands
* Values are clipped to keep them within valid range
* The noisy image is saved as a new GeoTIFF



---


---

### PatchMix (`patchmix=True`)

PatchMix replaces **one quadrant** of the clean image with its noisy version to create hybrid samples.
The image is split into four parts (top-left, top-right, bottom-left, bottom-right), and noise is inserted into one patch at a time.

### File Naming

The output files show where noise was added:

* `noise_tl.tif` → top-left
* `noise_tr.tif` → top-right
* `noise_bl.tif` → bottom-left
* `noise_br.tif` → bottom-right

---

This helps models learn localized noise and improves robustness.

---

## Run Locally

Clone the project:

```bash
git clone https://github.com/bdipesh3045/geospectral.git
cd geospectral
```

Install dependency:

```bash
pip install setuptools
```

Install the package:

```bash
pip install .
```

---



## Thank you!

---

Thank you for using **GeoSpectral**! 🎉
If you have any questions or feedback, feel free to reach out at **📧 [dipeshsharma9800@gmail.com](mailto:dipeshsharma9800@gmail.com)** ✨

---
