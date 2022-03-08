# Data Processing

This component converts the FHIR data present in the input-artifact to a more readable format based on resource type.

Prerequisites:
1. Must have AWS account
2. Create an S3 Bucket
3. Must run [Data upload S3](/src/components/data_upload_S3) to upload your data present on your local machine to S3
4. Must run [Data upload WandB](/src/components/data_upload_WandB) to link the S3 bucket & create an artifact for processing

# Parameters



You can change the parameters used in this component before running to make the running of the component easier.

Simply navigate to: [MLProject](/src/components/data_processing/MLproject)

For each parameter add below the "type":
    
    default: xxx

where xxx is your parameter as the input to the component

If you have added the default for few parameters, you will not need to input those parameters when running the script through terminal

**DO NOT CHANGE THE FOLLOWING PARAMETERS:
1. input_artifact
2. output_artifact
3. output_type**

# Run

1. Open the terminal
2. Activate conda environment through these [Instructions](/src/components/README.md)
3. Navigate to the projects' directory
4. Navigate to components directory:



    cd src/components/data_processing


5. Run the following code:
    
        mlflow run . -P AWS_ACCESS_KEY_ID=xxx \
                     -P AWS_SECRET_ACCESS_KEY=xxx \
                     -P AWS_SESSION_TOKEN=xxx \
                     -P AWS_DEFAULT_REGION=xxx \
                     -P input_artifact=xxx  \
                     -P output_directory=xxx \
                     -P output_artifact=xxx  \
                     -P output_type=xxx  \
                     -P output_description=xxx

