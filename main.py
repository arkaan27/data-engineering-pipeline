"""
Main function to run the script of the pipeline

Author: Arkaan Quanunga
Date: 03/03/2022

"""
import os
import tempfile
import mlflow
import hydra
import omegaconf

# The Steps this pipeline will run- edit this based on local machine vs S3
# storage
_steps = [
    # Comment this line out if you don't have any data on local machine &
    # already have data present on S3
    # "data_upload_S3",
    "data_upload",
    "data_processing",
    "database_upload"
]


@hydra.main(config_name='config')
def run_pipeline(config: omegaconf.DictConfig):
    """
    Running the entire pipeline flow

    :param config: Getting the dictionary from config file
    :return:
    """

    # Set up the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "data_upload_S3" in active_steps:
            # Upload files to S3 bucket
            _ = mlflow.run(
                os.path.join(
                    hydra.utils.get_original_cwd(),
                    "src",
                    "components",
                    "data_upload_S3"),
                "main",
                parameters={
                    "AWS_DEFAULT_REGION": config["main"]["AWS"]["DEFAULT_REGION_NAME"],
                    "bucket_name": config["data_upload_S3"]["bucket_name"],
                    "bucket_prefix": config["data_upload_S3"]["bucket_prefix"],
                    "dataset_path": config["data_upload_S3"]["path"],
                })

        if "data_upload" in active_steps:
            # Upload file and load in W&B
            _ = mlflow.run(
                os.path.join(
                    hydra.utils.get_original_cwd(),
                    "src",
                    "components",
                    "data_upload_WandB2"),
                "main",
                parameters={
                    "data_location": config["data_upload_S3"]["data_location"],
                    "bucket_path": "s3://" +
                    config['data_upload_S3']['bucket_name'] +
                    "/" +
                    config["data_upload_S3"]["bucket_prefix"],
                    "directory_path": config["data_upload_S3"]["directory_path"],
                    "output_artifact": "raw_data",
                    "output_type": "data_upload",
                    "output_description": "Artifact for storage of data on Weights & Biases",
                },
            )

        if "data_processing" in active_steps:
            # Process data by extracting crucial files from data uploaded
            _ = mlflow.run(
                os.path.join(
                    hydra.utils.get_original_cwd(),
                    "src",
                    "components",
                    "data_processing"),
                "main",
                parameters={
                    "AWS_DEFAULT_REGION": config["main"]["AWS"]["DEFAULT_REGION_NAME"],
                    "data_upload_type": config["data_upload_S3"]["data_upload_type"],
                    "bucket_name": config["data_upload_S3"]["bucket_name"],
                    "input_artifact": "raw_data:latest",
                    "output_directory": config["data_processing"]["output_directory"],
                    "output_artifact": "processed_data",
                    "output_type": "processed_data",
                    "output_description": "Processing the data by" +
                                          "separating json file to different files &" +
                                          " uploading processed data to S3",
                })

        if "database_upload" in active_steps:
            # Uploading Processed data to database
            _ = mlflow.run(
                os.path.join(
                    os.path.join(
                        hydra.utils.get_original_cwd(),
                        "src",
                        "components",
                        "database_upload")),
                "main",
                parameters={
                    "data_download_type": config["data_processing"]["data_upload_type"],
                    "MONGO_Cluster_name": config["main"]["MONGODB"]["MONGO_Cluster_name"],
                    "Database_name": config["database_upload"]["Database_name"],
                    "input_artifact": "processed_data:latest",
                    "output_artifact": "database_upload",
                    "output_type": "database_upload",
                    "output_description": "Uploading the processed data " +
                                          "to a MONGO DB database for query purposes"})


if __name__ == "__main__":
    run_pipeline()
