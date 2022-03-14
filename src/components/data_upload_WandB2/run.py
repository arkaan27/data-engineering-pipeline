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
import argparse
from Utils.wandbUtils import create_run, create_artifact, log_artifact, add_reference

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
    run = create_run(args, project_name="data_sample",
                     group="dev2",
                     job_type="data_upload")

    # Creating artifact
    logging.info("Creating Artifact")
    artifact = create_artifact(output_artifact=args.output_artifact,
                               output_type=args.output_type,
                               output_description=args.output_description)

    if args.data_location == "LOCAL":
        logging.info("Uploading dataset to Weights & Biases")
        artifact.add_dir(args.directory_path)
    elif args.data_location == "AWS_S3":
        logging.info("Adding S3 Bucket as reference")
        add_reference(artifact, args.bucket_path)

    # Logging artifact
    logging.info("Logging the artifact")
    log_artifact(run, artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data upload process to Weights & Biases")

    parser.add_argument(
        "--data_location",
        type=str,
        help="Choose: AWS_S3; LOCAL",
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
    parser.add_argument(
            "--bucket_path",
            type=str,
            help="Bucket path to upload data to Weights & Biases",
            required=False,
    )
    parser.add_argument(
            "--directory_path",
            type=str,
            help="Local path towards dataset upload data to Weights & Biases",
            required=False,
    )

    args = parser.parse_args()

    go(args)
