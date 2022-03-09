"""
Upload data directory to S3 Bucket and creating prefix if it does not exist

Requires:
1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY
3. AWS_DEFAULT_REGION
4. bucket_name
5. bucket_prefix
6. dataset_path

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


def bucket_exists(s3, bucket_name):
    """

    :param s3: Client of S3 initialised
    :param bucket_name: [str] The bucket name
    :return:
    """
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


def upload_directory(s3, path, bucket_name, prefix):
    """

    Uploading an entire directory of files to S3

    :param s3: Client of S3 Initialised
    :param path: [str] The path to the dataset directory to upload
    :param bucket_name: [str] The bucket name to upload data to
    :param prefix: [str] The prefix to create when uploading the data
    :return:
    """
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
    """
    Checks if the bucket exists & Uploads data to the bucket

    :param args: The parameters needed to run this function
    :return:
    """
    # Defining crucial variables
    os.environ['AWS_ACCESS_KEY_ID']=args.AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY']= args.AWS_SECRET_ACCESS_KEY

    # Creating S3 Resource From the Session.
    s3 = boto3.resource(
        service_name='s3',
        region_name=args.AWS_DEFAULT_REGION,
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )

    # Checking if the bucket exists
    bucket_exists(s3, args.bucket_name)

    # Uploading directory to the bucket
    upload_directory(s3, path=args.dataset_path, bucket_name=args.bucket_name, prefix=args.bucket_prefix)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Data upload process to S3")

    parser.add_argument(
        "--AWS_ACCESS_KEY_ID",
        type=str,
        help="Your AWS ACCESS KEY ID for accessing the bucket",
        required=True,
    )

    parser.add_argument(
        "--AWS_SECRET_ACCESS_KEY",
        type=str,
        help="Your AWS SECRET ACCESS KEY for accessing the bucket",
        required=True,
    )

    parser.add_argument(
        "--AWS_DEFAULT_REGION",
        type=str,
        help="Your AWS Default Region where the bucket is located",
        required=True,
    )

    parser.add_argument(
        "--bucket_name",
        type=str,
        help="Bucket name to upload data",
        required=True,
    )

    parser.add_argument(
        "--bucket_prefix",
        type=str,
        help="Bucket prefix to upload the data into it",
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
