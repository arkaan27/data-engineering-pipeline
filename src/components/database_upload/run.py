"""
Uploads processed data to Mongo DB database

Requires:
1. AWS ACCESS KEY ID [str] - Environment variable
2. AWS SECRET ACCESS KEY [str] - Environment variable
3. MONGO USERNAME [str] - Environment variable
4. MONGO PASSWORD [str] - Environment variable
5. MONGO CLUSTER NAME [str]
6. DATABASE NAME - Default as FHIR-data [str]
7. OUTPUT DESCRIPTION- Description of the artifact that is produced from this module


Author: Arkaan Quanunga
Date: 08/03/2022
"""

import logging
import wandb
import argparse
from Utils.wandbUtils import create_run,create_artifact, log_artifact, add_reference
from Utils.MongoDBUtils import mongo_initialize, create_db, insert_collections

# Basic Logging
logging.basicConfig(
    filename='logs/mongo_db_data_upload.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def go(args):
    # Creating a run instance
    logger.info("Creating the run on Weights & Biases")
    run = create_run(args,
                     project_name="data-engineering",
                     group="dev",
                     job_type="database_upload")

    # Downloading the artifact and logging
    logger.info("Downloading the artifact")
    data_dir = wandb.use_artifact(args.input_artifact).download()

    # Creating a client for Mongo DB
    logger.info("Creating Client for MongoDB using Credentials provided")
    client = mongo_initialize(args.MONGO_Cluster_name)

    # Creating database in the client
    logger.info("Creating Database: " + "{}".format(args.Database_name))
    database = create_db(client, args.Database_name)

    # Extracting contents to upload to database from the artifact
    logger.info("Uploading content to database")
    insert_collections(data_dir, database)

    logger.info("SUCCESS: Uploaded all content specified to Collection name")

    logger.info("Creating Output Artifact")
    artifact = create_artifact(args.output_artifact, args.output_type, args.output_description)

    logger.info("Referencing the database to Weights & Biases Artifact")
    database_uri = "mongodb+srv://username:password@{}.ppi15.mongodb.net/{}".format(args.MONGO_Cluster_name,
                                                                                    args.Database_name)
    artifact.add_reference(database_uri, name='database-uri')

    # Logging artifact
    logging.info("Logging the artifact")
    log_artifact(run, artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uploading Processed data to a MONGO DB Database Cluster")

    parser.add_argument(
        "--MONGO_Cluster_name",
        type=str,
        help="Your Mongo DB Cluster name to connect application to the database",
        required=True,
    )

    parser.add_argument(
        "--Database_name",
        type=str,
        help="Database name to create/update the records with",
        required=False,
    )

    parser.add_argument(
        "--data_download_type",
        type=str,
        help="AWS_S3 OR LOCAL",
        required=True,
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
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
