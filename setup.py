from setuptools import find_packages, setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geospectral",
    description="A Python package for augmenting geospatial raster data (GeoTIFFs) with various techniques including noise addition, patch mixing, and geometric transformations.",
    version="0.2.3",
    long_description=long_description,
    package_dir={"": "app"},
    packages=find_packages(where="app"),

    long_description_content_type="text/markdown",
    url="https://github.com/bdipesh3045/geospectral",
    author="Dipesh Sharma",
    author_email="dipeshsharma9800@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "rasterio",
        "fiona",
        "pandas"
    ],
   
    python_requires=">=3.10",
)