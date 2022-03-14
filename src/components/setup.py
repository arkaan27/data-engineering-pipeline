from setuptools import setup

setup(
    name="Utils",
    version=0.1,
    description="Utilities for making the program function",
    zip_safe=False,  # avoid eggs, which make the handling of package data cumbersome
    packages=["data_upload_S3", "Utils"],
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
