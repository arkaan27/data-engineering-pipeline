# Data Upload S3

This component uploads local data to S3. It can be reused in other pipelines as package.

Prerequisites:
1. AWS Account Setup
2. S3 bucket to upload data 
3. data on your local machine

# Parameters

You can change the parameters used in this component before running to make the running of the component easier.

Simply navigate to: [MLProject](/src/components/data_upload_S3/MLproject)

For each parameter add below the "type":
    
    default: xxx

where xxx is your parameter as the input to the component

If you have added the default for few parameters, you will not need to input those parameters when running the script through terminal

**You are allowed to add all parameters in this component with default types**

# Run

1. Open the terminal
2. Activate conda environment through these [Instructions](/src/components/README.md)
3. Navigate to the projects' directory
4. Navigate to components directory:



    cd src/components/data_upload_S3

5. Run the following code:
    
        mlflow run . -P AWS_ACCESS_KEY_ID=xxx \
                     -P AWS_SECRET_ACCESS_KEY=xxx \
                     -P AWS_DEFAULT_REGION=xxx \
                     -P bucket_name=xxx \
                     -P bucket_prefix=xxx  \
                     -P dataset_path=xxx \

Replace xxx with your keys and names

If all variables has been added to the [MLProject](MLproject) file as default then run the following code:

        mlflow run .
