import os
import fiona
import rasterio
from rasterio.mask import mask
from concurrent.futures import ThreadPoolExecutor
from functools import partial

def clip_one_feature(feature, i, tiff_file, output_dir):
    shapes = [feature["geometry"]]

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


def clip_raster_threaded(shapefile_path, tiff_file, output_dir, workers=None):
    if (workers is None):
        workers = min(8, os.cpu_count() * 2)
        print(f"Using {workers} workers for threading.")
    os.makedirs(output_dir, exist_ok=True)

    # Read all features once (Fiona is NOT thread-safe)
    with fiona.open(shapefile_path, "r") as shapefile:
        features = list(shapefile)

    # Create a worker function with fixed args
    worker = partial(clip_one_feature, tiff_file=tiff_file, output_dir=output_dir)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(lambda args: worker(*args), [(f, i) for i, f in enumerate(features)])

    print("✅ All regions clipped successfully.")



def clip_raster_serial(shapefile_path, tiff_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with fiona.open(shapefile_path, "r") as shapefile:
        for i, feature in enumerate(shapefile):
            shapes = [feature["geometry"]]

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