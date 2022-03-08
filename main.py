"""
Main function to run the script of the pipeline

Author: Arkaan Quanunga
Date: 03/03/2022

"""
import json

import mlflow
import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig

# The Steps this pipeline will run- edit this based on local machine vs S3 storage
_steps = [
    "data_upload_S3", # Comment this out if you dont have any data on local machine & already have data present on S3
    "data_upload",
    "data_processing",
    "database_upload"
]


@hydra.main(config_name='config')
def go(config: DictConfig):

    # Set up the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]
    os.environ["AWS_ACCESS_KEY_ID"]= config["main"]["AWS"]["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = config["main"]["AWS"]["AWS_SECRET_ACCESS_KEY"]
    os.environ["AWS_SESSION_TOKEN"]= config["main"]["AWS"]["AWS_SESSION_TOKEN"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "data_upload_S3" in active_steps:
            # Upload files to S3 bucket
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(),"src","components", "data_upload_S3"),
                "main",
                parameters={
                    "AWS_ACCESS_KEY_ID": config["main"]["AWS"]["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": config["main"]["AWS"]["AWS_SECRET_ACCESS_KEY"],
                    "AWS_DEFAULT_REGION": config["main"]["AWS"]["AWS_DEFAULT_REGION"],
                    "bucket_name": config["data_upload_S3"]["bucket_name"],
                    "bucket_prefix": config["data_upload_S3"]["bucket_prefix"],
                    "dataset_path": config["data_upload_S3"]["path"],
                }
            )

        if "data_upload" in active_steps:
            # Upload file and load in W&B
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "components","data_upload_WandB"),
                "main",
                parameters={
                    "AWS_ACCESS_KEY_ID": config["main"]["AWS"]["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": config["main"]["AWS"]["AWS_SECRET_ACCESS_KEY"],
                    "bucket_path": "s3://"+config['data_upload_S3']['bucket_name']+"/"+config["data_upload_S3"]["bucket_prefix"],
                    "output_artifact": "raw_data",
                    "output_type": "data",
                    "output_description": "Artifact for storage of data on Weights & Biases",
                },
            )
        if "data_processing" in active_steps:
            # Process data by extracting crucial files from data uploaded
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(),"src", "components", "data_processing"),
                "main",
                parameters={
                    "AWS_ACCESS_KEY_ID": config["main"]["AWS"]["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": config["main"]["AWS"]["AWS_SECRET_ACCESS_KEY"],
                    "AWS_SESSION_TOKEN": config["main"]["AWS"]["AWS_SESSION_TOKEN"],
                    "AWS_DEFAULT_REGION": config["main"]["AWS"]["AWS_DEFAULT_REGION"],
                    "input_artifact": "raw_data:latest",
                    "output_directory": config["data_processing"]["output_directory"],
                    "output_artifact": "processed_data",
                    "output_type": "processed_data",
                    "output_description": "Processing the data by seperating json file to different files & uploading processed data to S3",
                }
            )

        if "database_upload" in active_steps:
            # Uploading Processed data to database
            _ = mlflow.run(
                os.path.join(os.path.join(hydra.utils.get_original_cwd(),"src", "components", "database_upload")),
                "main",
                parameters={
                    "AWS_ACCESS_KEY_ID": config["main"]["AWS"]["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": config["main"]["AWS"]["AWS_SECRET_ACCESS_KEY"],
                    "MONGO_Username": config["main"]["MONGODB"]["MONGO_Username"],
                    "MONGO_Password": config["main"]["MONGODB"]["MONGO_Password"],
                    "MONGO_Cluster_name": config["main"]["MONGODB"]["MONGO_Cluster_name"],
                    "Database_name": config["database_upload"]["Database_name"],
                    "input_artifact": "processed_data:latest",
                    "output_artifact": "database_upload",
                    "output_type": "database",
                    "output_description": "Uploading the processed data to a MONGO DB database for query purposes"
                }
            )


if __name__ == "__main__":
    go()
