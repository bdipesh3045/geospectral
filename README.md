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
```python
# Basic usage example
from geospectral import clip_raster

clip_raster(tif_file, shapefile, output_path, threaded=True)
```

## Installation
```bash
pip install geospectral
```
