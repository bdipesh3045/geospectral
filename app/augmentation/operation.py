import numpy as np
import os
import rasterio





def add_gaussian_noise_tif(
    input_tif: str,
    output_tif: str,
    noise_std: float,
    normalize: bool = True
):
    """
    Adds Gaussian noise to each band of a multispectral GeoTIFF.

    Args:
        input_tif (str): Path to the input GeoTIFF.
        output_tif (str): Path to save the noisy GeoTIFF.
        noise_std (float): Standard deviation of the Gaussian noise (in normalized range).
        normalize (bool): Whether to normalize pixel values to [0, 1] before adding noise.
    """

    # Load the image
    with rasterio.open(input_tif) as src:
        img = src.read().astype(np.float32)  # (bands, H, W)
        meta = src.meta

    # Normalize per band (if requested)
    if normalize:
        for b in range(img.shape[0]):
            band = img[b]
            bmin, bmax = np.nanpercentile(band, (2, 98))
            img[b] = np.clip((band - bmin) / (bmax - bmin + 1e-8), 0, 1)

    # Add Gaussian noise
    noise = np.random.randn(*img.shape) * noise_std
    noisy_img = np.clip(img + noise, 0, 1)

    # Save the result
    meta.update(dtype='float32')
    with rasterio.open(output_tif, "w", **meta) as dst:
        dst.write(noisy_img.astype(np.float32))

    print(f"✅ Gaussian noise added and saved to: {output_tif}")




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
    print(f"✅ Gaussian Noise Added: {path}")




def geometric_augmentations(image_path:str, aug_type:list, apply_all: bool = False,noise:int=0):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = base_name
    os.makedirs(output_dir, exist_ok=True)

    if noise!=0:
        noisy_output_path = os.path.join(
            output_dir,
            f"{base_name}_NOISY.tif"
        )
        add_gaussian_noise_tif(
            input_tif=image_path,
            output_tif=noisy_output_path,
            noise_std=noise
        )

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
