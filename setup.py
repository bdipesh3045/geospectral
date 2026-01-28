from setuptools import find_packages, setup

setup(
    name="augmentation",
    version="0.0.10",
    description=open("README.md").read(),
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