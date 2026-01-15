import fiona
import pandas as pd
import rasterio
from rasterio.mask import mask
import os


def clip_raster(shapefile_path, tiff_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with fiona.open(shapefile_path, 'r') as shapefile:
        for i, feature in enumerate(shapefile):
            shapes = [feature['geometry']]
            feature_id = feature['id']


            with rasterio.open(tiff_file) as src:
                out_image, out_transform = mask(src, shapes, crop=True)
                out_meta = src.meta.copy()


            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })


            output_tiff = os.path.join(output_dir, f"clip_{i+1}.tif")
            with rasterio.open(output_tiff, "w", **out_meta) as dest:
                dest.write(out_image)

            print(f"Saved: {output_tiff}")

print("✅ All regions clipped successfully.")