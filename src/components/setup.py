from setuptools import setup


setup(
    name="data_upload_S3",
    version=0.1,
    description="Utilities for uploading data to S3 bucket",
    zip_safe=False,  # avoid eggs, which make the handling of package data cumbersome
    packages=["data_upload_S3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "mlflow",
        "wandb",
        "boto3"
    ]
)

setup(
    name="Utils",
    version=0.1,
    description="Utilities for the programme to run",
    zip_safe=False,  # avoid eggs, which make the handling of package data cumbersome
    packages=["Utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "mlflow",
        "wandb",
        "pymongo"
    ]
)