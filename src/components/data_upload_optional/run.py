"""
Upload data files to S3 bucket

Author: Arkaan Quanunga
Date: 04/03/2022

"""

import os
import logging
import boto3
import wandb
import argparse
from botocore.exceptions import ClientError

# Basic Logging
logging.basicConfig(
    filename='logs/data_upload_results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)

# Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id='<your_access_key_id>',
    aws_secret_access_key='<your_secret_access_key>'
)

# Creating S3 Resource From the Session.
s3 = session.resource('s3')


def bucket_exists(bucket_name):
    # Logging the bucketname for reference
    logging.info("Bucket name: {}".format(bucket_name))

    # Making sure bucket_name is a string
    try:
        assert isinstance(bucket_name, str)
    except AssertionError:
        logging.error("ERROR: Bucket name is not a string value")

    # Making sure bucket name exists on s3

    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError:
        logging.error("ERROR: Bucket name does not exist")


def upload_directory(path, bucket_name):
    # Asserting the path & bucket_name to be string
    try:
        assert isinstance(path, str)
    except AssertionError:
        logging.error("ERROR: File path is not a string type")

    try:
        assert isinstance(bucket_name, str)
    except AssertionError:
        logging.error("ERROR: Bucket name is not a string type")

    # Checking if file path exists
    if os.path.exists(path):
        logging.info("SUCCESS: The file path specified exists!")
    else:
        logging.error("ERROR: File path does not exist!")

    # Uploading the files to S3 bucket
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                s3.meta.client.upload_file(os.path.join(root, file), bucket_name, "FHIR-data/{}".format(file))
        logging.info("SUCCESS: Files Uploaded Successfully")
    except:
        logging.error("ERROR: Files could not be uploaded, check s3 bucket")


def go(args):
    # Creating a WandB run for automating pipeline
    run = wandb.init(project="data-engineering", group="dev", job_type="data_upload")
    run.config.update(args)

    # Creating artifact
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    # Adding directory to the WandB
    artifact.add_dir(args.directory_path)

    # Logging artifact
    logging.info("Logging the artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of the artifact name to be outputted",
        required=True,
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of artifact to be outputted",
        required=True,
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    parser.add_argument(
        "--directory_path",
        type=str,
        help="Directory file path to upload",
        required=True,
    )

    args = parser.parse_args()

    go(args)
