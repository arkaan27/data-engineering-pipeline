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

_steps = [
    "data_upload",
    "data_processing",
    "data_check",
    "database_write"
]


@hydra.main(config_name='config')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    if "data_upload" in active_steps:
        # Upload file and load in W&B
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(), "src", "components","data_upload_WandB"),
            "main",
            parameters={
                "bucket_path": config['data_upload']['bucket_path'],
                "output_artifact": "raw_data",
                "output_type": "data_upload",
                "output_description": "Artifact for storage of data on Weights & Biases",
            },
        )


if __name__ == "__main__":
    go()
