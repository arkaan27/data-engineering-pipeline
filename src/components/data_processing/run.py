#!/usr/bin/env python
"""
Download from WandB the raw dataset and convert it to tabular format, exporting the result to a new artifact

Author: Arkaan Quanunga
Date: 04/03/2022

"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    # Creating a run instance
    run = wandb.init(project="data_pipeline",group= "dev",job_type="data_processing")
    run.config.update(args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Data processing step to convert FHIR to tabular format")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualifed name for the input artifact",
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