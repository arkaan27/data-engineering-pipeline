"""
Utilities of Weights & Biases for re-usability

Author: Arkaan Quanunga
Date: 13/03/2022
"""

import wandb


def create_run(args, project_name, group, job_type):
    """

    :param args:
    :param project_name:
    :param group:
    :param job_type:
    :return:
    """
    run = wandb.init(project=project_name,
                     group=group,
                     job_type=job_type
                     )
    run.config.update(args)

    return run


def create_artifact(output_artifact, output_type, output_description):
    """

    :param output_artifact:
    :param output_type:
    :param output_description:
    :return:
    """
    artifact = wandb.Artifact(output_artifact,
                              type=output_type,
                              description=output_description
                              )
    return artifact


def add_reference(artifact, reference):
    """

    :param artifact:
    :param reference:
    :return:
    """
    artifact.add_reference(reference)


def log_artifact(run, artifact):
    """

    :param run:
    :param artifact:
    :return:
    """
    run.log_artifact(artifact)
