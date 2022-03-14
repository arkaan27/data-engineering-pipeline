#!/usr/bin/env python
"""
Download from WandB the raw dataset and extract different resource types, exporting the result to a new artifact

Requirements:
1. AWS_ACCESS_KEY_ID -  Environment Variable
2. AWS_SECRET_ACCESS_KEY - Environment Variable
3. AWS_DEFAULT_REGION
4. Input_artifact containing the dataset to be processed
5. output_artifact- name of the output artifact that is going to be produced - Default: processed_data
6. output_type- default: processed_data
7. output_description- the description of the artifact for reference

Update: Converting function to modular code - 11/03/2022 - Check src.components.Utils

Author: Arkaan Quanunga
Date: 04/03/2022

"""
import os
import argparse
import logging
from data_upload_S3.run import bucket_exists, upload_directory, initialize_client, run_process
from Utils.wandbUtils import create_run, add_reference, create_artifact, log_artifact
from Utils.Data_processing_Utils import create_directory, process_files
import wandb

# Basic Logging

logging.basicConfig(
    filename='logs/data_process_results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def go(args):
    logger.info("Creating the run on Weights & Biases")

    run = create_run(args,
                     project_name="data-engineering",
                     group="dev",
                     job_type="data_processing")

    logger.info("Downloading the artifact")
    data_dir = wandb.use_artifact(args.input_artifact).download()

    logger.info("Creating the directory for output files")
    create_directory(args.output_directory)

    logging.info("Checking if Processing has been completed already")
    if len(os.listdir(args.output_directory)) == 0:
        # Looping overall the files in the directory
        logger.info("Processing files...")
        process_files(args.output_directory, data_dir)

    logger.info("SUCCESS: Processing Files Completed")

    logger.info("Creating AWS Session for Accessing S3 & uploading data to S3")
    run_process(args)
    logger.info("SUCCESS: Uploaded data to S3 successfully")

    logger.info("Creating Output Artifact")
    artifact = create_artifact(output_artifact=args.output_artifact,
                               output_type=args.output_type,
                               output_description=args.output_description)

    # Referencing the data to the new artifact
    if args.data_upload_type == "LOCAL":
        logger.info("Uploading the files to the artifact")
        artifact.add_dir(args.output_directory)
    elif args.data_upload_type == "AWS_S3":
        logger.info("Referencing the S3 bucket data to Weights & Biases Artifact")
        bucket_path = "s3://" + args.bucket_name + "/" + args.output_directory
        add_reference(artifact, reference=bucket_path)

    # Logging artifact
    logging.info("Logging the artifact")
    log_artifact(run, artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data processing step to extract data from FHIR format")

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
