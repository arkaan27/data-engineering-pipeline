#!/usr/bin/env python
"""
Download from WandB the raw dataset and extract different resource types, exporting the result to a new artifact

Author: Arkaan Quanunga
Date: 04/03/2022

"""
import os
import json
import argparse
import logging
import boto3
from botocore.exceptions import ClientError
import wandb
from collections import defaultdict
from data_upload_S3.run import bucket_exists, upload_directory

# Basic Logging
logging.basicConfig(
    filename='logs/data_process_results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def go(args):
    # Creating a run instance
    logger.info("Creating the run on Weights & Biases")
    run = wandb.init(project="data-engineering", group="dev", job_type="data_processing")

    # Updating the parameters using arguments input
    logger.info("Updating the Parameters from input")
    run.config.update(args)

    # Downloading the artifact and logging
    logger.info("Downloading the artifact")
    data_dir = wandb.use_artifact(args.input_artifact).download()

    # Creating output dir for the processed data
    logger.info("Creating the directory for output files")
    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)

    # Looping overall the files in the directory
    logger.info("Processing files...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:

                # Reading the file
                extracted_data = json.load(f)

                # Extracting entries of the file
                entries = extracted_data['entry']

                # Creating set & dictionary
                resource_types = set()
                entry_resources = defaultdict(list)

                # Extracting data to dictionary based on resource type
                for resource in entries:
                    resource_type = resource["resource"]["resourceType"]
                    resource_types.add(resource_type)
                    resource_file_path = args.output_directory + "/" + f"{resource_type}.json"
                    entry_resources[resource_file_path].append(resource)

                for resource_file_path, resources in entry_resources.items():
                    if os.path.exists(resource_file_path):
                        # Getting existing contents of each resource
                        with open(resource_file_path, 'r') as i:
                            contents = json.load(i)

                        contents.extend(resources)
                    else:
                        contents = resources

                    # Saving it to output dir
                    with open(resource_file_path, 'w') as j:
                        json.dump(contents, j)

    # Logging Success of looping
    logger.info("SUCCESS: Processing Files Completed")

    # Creating AWS Session
    logger.info("Creating AWS Session for Accessing S3")
    s3 = boto3.resource(
        service_name='s3',
        region_name=args.AWS_DEFAULT_REGION,
        aws_access_key_id=args.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=args.AWS_SECRET_ACCESS_KEY,
    )

    # Adding Processed Files to S3
    logger.info("Uploading directory to S3")
    bucket_exists(s3, args.bucket_name)
    upload_directory(s3, os.path.join(os.getcwd(), args.output_directory), args.bucket_name, args.output_directory)

    # Creating output artifact
    logger.info("Creating Output Artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    # Referencing the data to the new artifact
    logger.info("Referencing the S3 bucket data to Weights & Biases Artifact")
    artifact.add_reference(args.bucket_path)

    # Logging artifact
    logging.info("Logging the artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data processing step to extract data from FHIR format")

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
        "--AWS_SESSION_TOKEN",
        type=str,
        help="Your AWS Session Token for accessing the bucket",
        required=False,
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
        help="The bucket name to upload the data",
        required=True,
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--output_directory",
        type=str,
        help="Output directory for processed data to be stored on local machine",
        required=True,
    )

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

    args = parser.parse_args()

    go(args)
