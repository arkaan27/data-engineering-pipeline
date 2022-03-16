import os
import pytest
import pandas as pd

from Utils.wandUtils import create_run, create_artifact, log_artifact, add_reference

@pytest.fixture
def creating_run():
    args = []
    run = create_run(args,
                     project_name="data-engineering",
                     group="test",
                     job_type="testing")

    return run

@pytest.fixture()
def creating_artifact():
    artifact = create_artifact(output_artifact="test_artifact",
                               output_type="test_data",
                               output_description="sample-test")

    return artifact


@pytest.fixture()
def data():
    """10 sample data for test"""

    dirname = os.path.dirname(__file__)
    df = pd.read_json(os.path.join(dirname, "data"))[:10]
    return df


def test_data_location(creating_artifact,creating_run):

    run = creating_run()
    artifact = creating_artifact()

    artifact.add_file("xxx")


