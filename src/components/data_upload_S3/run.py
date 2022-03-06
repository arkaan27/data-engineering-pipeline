"""
Upload data to S3 Bucket

Make sure the environment variables consists of

1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY

Author: Arkaan Quanunga
Date: 04/03/2022
"""
import os
import logging
import boto3
from botocore.exceptions import ClientError
import argparse

# Basic Logging
logging.basicConfig(
    filename='logs/data_upload_S3_results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)

# Creating S3 Resource From the Session.
s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-2',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)


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


def upload_directory(path, bucket_name, prefix):
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
                s3.meta.client.upload_file(os.path.join(root, file), bucket_name, "{}/{}".format(prefix, file))
        logging.info("SUCCESS: Files Uploaded Successfully")
    except:
        logging.error("ERROR: Files could not be uploaded, check s3 bucket")


def go(args):

    bucket_exists(args.bucket_name)
    upload_directory(args.dataset_path, args.bucket_name, args.bucket_prefix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data upload process to S3")

    parser.add_argument(
        "--bucket_prefix",
        type=str,
        help="Bucket prefix to upload the data into it",
        required=True,
    )

    parser.add_argument(
        "--bucket_name",
        type=str,
        help="Bucket name to upload data",
        required=True,
    )

    parser.add_argument(
        "--dataset_path",
        type=str,
        help="The directory path to upload data from",
        required=True,
    )

    args = parser.parse_args()

    go(args)
