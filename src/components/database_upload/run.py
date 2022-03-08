"""
Uploads processed data to Mongo DB database

Requires:
1. AWS ACCESS KEY ID [str]
2. AWS SECRET ACCESS KEY [str]
3. MONGO USERNAME [str]
4. MONGO PASSWORD [str]
5. MONGO CLUSTER NAME [str]
6. DATABASE NAME - Default as FHIR-data [str]
7. OUTPUT DESCRIPTION- Description of the artifact that is produced from this module


Author: Arkaan Quanunga
Date: 08/03/2022
"""

import os
import logging
import wandb
import pymongo
import json
import argparse

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
    run = wandb.init(project="data-engineering",
                     group="dev",
                     job_type="database_upload")

    # Updating the parameters using arguments input
    logger.info("Updating the Parameters from input")
    run.config.update(args)

    # Adding AWS Credentials to the environment

    os.environ["AWS_ACCESS_KEY_ID"]= args.AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = args.AWS_SECRET_ACCESS_KEY

    # Downloading the artifact and logging
    logger.info("Downloading the artifact")
    data_dir= wandb.use_artifact(args.input_artifact).download()

    # Creating a client for Mongo DB
    logger.info("Creating Client for MongoDB using Credentials provided")
    client = pymongo.MongoClient("mongodb+srv://{}:{}@{}.ppi15.mongodb.net".format(args.MONGO_Username,
                                                                                   args.MONGO_Password,
                                                                                   args.MONGO_Cluster_name,
                                                                                   args.Database_name))

    # Creating database in the client
    logger.info("Creating Database: " + "{}".format(args.Database_name))
    mydb = client[args.Database_name]

    # Extracting contents to upload to database from the artifact
    logger.info("Extracting content to upload to database")
    for root, dir,files in os.walk(data_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                resources = json.load(f)

            content_save= []

            # Removing a single nesting in the files
            for resource in resources:
                res= resource["resource"]
                url= resource["fullUrl"]
                resource["fullUrl"]= url
                content_save.append(res)


            # Creating collection name from file_names

            size= len(file)
            collection_name = file[:size-5]

            # Inserting content to the database collection
            mydb[collection_name].insert_many(content_save)

    logger.info("SUCCESS: Uploaded all content specified to Collection name")

    # Creating output artifact
    logger.info("Creating Output Artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    # Referencing the data to the new artifact
    logger.info("Referencing the database to Weights & Biases Artifact")
    database_uri= "mongodb+srv://username:password@{}.ppi15.mongodb.net/{}".format(args.MONGO_Cluster_name,
                                                                                   args.Database_name)
    artifact.add_reference(database_uri,name= 'database-uri')

    # Logging artifact
    logging.info("Logging the artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uploading Processed data to a MONGO DB Database Cluster")

    parser.add_argument(
        "--AWS_ACCESS_KEY_ID",
        type=str,
        help="Your AWS ACCESS KEY ID TO ACCESS THE BUCKET",
        required=True,
    )

    parser.add_argument(
        "--AWS_SECRET_ACCESS_KEY",
        type=str,
        help="Your AWS SECRET ACCESS KEY TO ACCESS THE BUCKET",
        required=True,
    )

    parser.add_argument(
        "--MONGO_Username",
        type=str,
        help="Your Mongo Username to connect to the Mongo DB",
        required=True,
    )

    parser.add_argument(
        "--MONGO_Password",
        type=str,
        help="Your Mongo password to connect to the Mongo DB",
        required=True,
    )

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







