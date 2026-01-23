# =====================================================
# Required Imports
# =====================================================
import os
import numpy as np
import rasterio


# =====================================================
# Load GeoTIFF Helper
# =====================================================
def load_tif(path: str):
    """
    Load a GeoTIFF as a float32 NumPy array.

    Returns:
        img  : np.ndarray (C, H, W)
        meta : rasterio metadata
    """
    with rasterio.open(path) as src:
        img = src.read().astype(np.float32)
        meta = src.meta.copy()
    return img, meta


# =====================================================
# Deterministic PatchMix (fixed quadrant)
# =====================================================
def patchmix_with_fixed_quadrant(
    clean: np.ndarray,
    noisy: np.ndarray,
    quadrant_index: int
):
    """
    Replace one quadrant of the clean image with the noisy image.

    quadrant_index:
        0 = top-left
        1 = top-right
        2 = bottom-left
        3 = bottom-right
    """
    C, H, W = clean.shape
    hmid, wmid = H // 2, W // 2

    clean_patches = [
        clean[:, :hmid, :wmid],
        clean[:, :hmid,  wmid:],
        clean[:,  hmid:, :wmid],
        clean[:,  hmid:,  wmid:],
    ]

    noisy_patches = [
        noisy[:, :hmid, :wmid],
        noisy[:, :hmid,  wmid:],
        noisy[:,  hmid:, :wmid],
        noisy[:,  hmid:,  wmid:],
    ]

    clean_patches[quadrant_index] = noisy_patches[quadrant_index]

    top = np.concatenate([clean_patches[0], clean_patches[1]], axis=2)
    bottom = np.concatenate([clean_patches[2], clean_patches[3]], axis=2)

    return np.concatenate([top, bottom], axis=1)


# =====================================================
# Main Function — YOU provide the paths
# =====================================================
def patchmix_from_paths(
    clean_tif_path: str,
    noisy_tif_path: str,
    output_dir: str = "patchmix_outputs"
):
    os.makedirs(output_dir, exist_ok=True)

    print(f"🔹 Loading clean image: {clean_tif_path}")
    clean, meta = load_tif(clean_tif_path)

    print(f"🔹 Loading noisy image: {noisy_tif_path}")
    noisy, _ = load_tif(noisy_tif_path)

    if clean.shape != noisy.shape:
        raise ValueError("Clean and noisy images must have identical shapes")

    meta.update(dtype="float32")

    # 🔑 Your requested naming
    quadrant_map = {
        "noise_tl": 0,  # top-left
        "noise_tr": 1,  # top-right
        "noise_bl": 2,  # bottom-left
        "noise_br": 3,  # bottom-right
    }

    for name, idx in quadrant_map.items():
        print(f"🔹 Creating PatchMix ({name})")
        hybrid = patchmix_with_fixed_quadrant(clean, noisy, idx)

        out_path = os.path.join(output_dir, f"{name}.tif")

        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(hybrid.astype(np.float32))

        print(f"✅ Saved: {out_path}")

    print("🎉 PatchMix completed with quadrant-specific noise names!")
