# geospectral
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
```

## Installation
```bash
pip install geospectral
```
