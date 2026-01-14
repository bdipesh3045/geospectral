import rasterio
import numpy as np

def describe_tiff(path):
    """
    Analyzes a multispectral TIFF and returns a dictionary of metrics.
    Also prints a clean summary to the console.
    """
    summary = {}

    with rasterio.open(path) as src:
        # 1. Basic Metadata
        summary['filename'] = path
        summary['shape'] = (src.count, src.height, src.width)  # (Bands, H, W)
        summary['crs'] = str(src.crs)
        summary['dtype'] = src.dtypes[0]  # Assuming all bands have same type
        summary['bounds'] = src.bounds
        
        # 2. Read the image data to calculate stats
        # (Note: For massive 10GB+ images, use a sample instead of src.read())
        data = src.read()
        
        # 3. Calculate Stats Per Band
        band_stats = []
        for i, band_data in enumerate(data):
            # Mask out "No Data" values if they exist
            if src.nodata is not None:
                # Create a masked array where the nodata value is ignored
                band_data = np.ma.masked_equal(band_data, src.nodata)

            stats = {
                "band_idx": i + 1,
                "min": float(band_data.min()),
                "max": float(band_data.max()),
                "mean": float(band_data.mean()),
                "std_dev": float(band_data.std())
            }
            band_stats.append(stats)
            
        summary['bands'] = band_stats

    # --- Print a Pretty Report ---
    print(f"--- IMAGE REPORT: {path} ---")
    print(f"Dimensions (Bands, H, W): {summary['shape']}")
    print(f"Data Type: {summary['dtype']}")
    print(f"Coordinate System: {summary['crs']}")
    print("-" * 40)
    print(f"{'Band':<6} | {'Min':<10} | {'Max':<10} | {'Mean':<10} | {'Std Dev':<10}")
    print("-" * 40)
    
    for b in band_stats:
        print(f"{b['band_idx']:<6} | {b['min']:<10.2f} | {b['max']:<10.2f} | {b['mean']:<10.2f} | {b['std_dev']:<10.2f}")
        
    print("-" * 40)
    
    # 4. Automatic Warnings (Based on the article's advice)
    if 'float' in summary['dtype'] and band_stats[0]['max'] > 1.0:
        print("⚠️  WARNING: Data is Float but values > 1.0. Is this Radiance? Be careful normalizing.")
    elif 'int' in summary['dtype'] and band_stats[0]['max'] <= 1:
        print("⚠️  WARNING: Data is Integer but values are small (0-1). Is this a binary mask?")
        
    return summary