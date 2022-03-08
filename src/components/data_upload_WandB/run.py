"""
Sync data files from S3 to Weights & Biases

Make sure to add:

1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY

to your environment Variables, see README.md of this component for more details

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

def go(args):
    # Creating a WandB run for automating pipeline
    logging.info("Creating the Weights and biases Run")
    run = wandb.init(project="data-engineering",
                     group="dev",
                     job_type="data_upload",
                     )
    #  Updating parameters of the run from the arguments taken
    logging.info("Updating the parameters of the run")
    run.config.update(args)

    # Adding AWS Credentials to the environment
    os.environ["AWS_ACCESS_KEY_ID"]= args.AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"]= args.AWS_SECRET_ACCESS_KEY

    # Creating artifact
    logging.info("Creating Artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    # Adding the S3 directory to the artifact
    logging.info("Adding S3 Bucket as reference")
    artifact.add_reference(args.bucket_path)

    # Logging artifact
    logging.info("Logging the artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data upload process to Weights & Biases")


    parser.add_argument(
        "--AWS_ACCESS_KEY_ID",
        type=str,
        help="Your AWS ACCESS KEY ID for accessing the bucket",
        required=True,
    )

    parser.add_argument(
        "--AWS_SECRET_ACCESS_KEY",
        type=str,
        help="Your AWS Secret Access Key for accessing the bucket",
        required=True,
    )

    parser.add_argument(
        "--bucket_path",
        type=str,
        help="Bucket path to upload data to Weights & Biases",
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
