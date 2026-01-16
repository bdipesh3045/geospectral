import numpy as np
import os
import rasterio


def save_tif(image, profile, path, original_min=None, original_max=None):
    """Save a numpy array as GeoTIFF with correct scaling."""
    profile = profile.copy()
    profile.update({
        "count": image.shape[0],
        "height": image.shape[1],
        "width": image.shape[2],
    })

    dtype = np.dtype(profile['dtype'])

    # Restore to original range if given
    if original_min is not None and original_max is not None:
        image = image * (original_max - original_min) + original_min

    with rasterio.open(path, 'w', **profile) as dst:
        dst.write(image.astype(dtype))
    print(f"✅ Saved: {path}")




def geometric_augmentations(image_path, aug_type, apply_all=False):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = base_name
    os.makedirs(output_dir, exist_ok=True)

    # Open image once
    with rasterio.open(image_path) as src:
        data = src.read()
        profile = src.profile.copy()

    dtype = np.dtype(profile["dtype"])

    # Normalize if integer type
    if np.issubdtype(dtype, np.integer):
        original_min, original_max = data.min(), data.max()
        data = (data - original_min) / (original_max - original_min)
    else:
        original_min = original_max = None

    original_out_path = os.path.join(
            output_dir,
            f"{base_name}_ORIG.tif"
        )
    save_tif(data, profile, original_out_path, original_min, original_max)




    # Store (name, function)
    aug_operations = []

    if "H" in aug_type or apply_all:
        aug_operations.append(("H", lambda x: np.flip(x, axis=2)))
    if "V" in aug_type or apply_all:
        aug_operations.append(("V", lambda x: np.flip(x, axis=1)))
    if "R" in aug_type or apply_all:
        aug_operations.append(("R", lambda x: np.rot90(x, k=1, axes=(1, 2))))
    if "R2" in aug_type or apply_all:
        aug_operations.append(("R2", lambda x: np.rot90(x, k=2, axes=(1, 2))))
    if "R3" in aug_type or apply_all:
        aug_operations.append(("R3", lambda x: np.rot90(x, k=3, axes=(1, 2))))
    for name, func in aug_operations:
        aug_data = func(data)

        out_path = os.path.join(
            output_dir,
            f"{base_name}_{name}.tif"
        )

        save_tif(aug_data, profile, out_path, original_min, original_max)

    print("🎉 All geometric augmentations completed!")
