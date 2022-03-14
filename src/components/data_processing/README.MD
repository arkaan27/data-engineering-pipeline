# Data Processing

This component converts the FHIR data present in the input-artifact to a more readable format based on resource type.

Prerequisites:
1. Must run [Data upload WandB](/src/components/data_upload_WandB2) to link the S3 bucket & create an artifact for processing
2. Can provide AWS Credentials & S3 details if you want to upload data to S3
# Parameters

You can change the parameters used in this component before running to make the running of the component easier.

Simply navigate to: [MLProject](/src/components/data_processing/MLproject)

For each parameter add below the "type":
    
    default: xxx

where xxx is your parameter as the input to the component

If you have added the default for few parameters, you will not need to input those parameters when running the script through terminal

**DO NOT CHANGE THE FOLLOWING PARAMETERS:**
1. input_artifact
2. output_artifact
3. output_type


# Run

1. Open the terminal
2. Activate conda environment through these [Instructions](/src/components/README.md)
3. Navigate to the projects' directory
4. Navigate to components directory:



    cd src/components/data_processing


5. Run the following code:
    
        mlflow run . -P AWS_DEFAULT_REGION=xxx \
                     -P data_upload_type==xxx \
                     -P input_artifact=xxx  \
                     -P output_directory=xxx \
                     -P output_artifact=xxx  \
                     -P output_type=xxx  \
                     -P output_description=xxx

If you have put data_upload_type as AWS_S3, please add environment variables:

1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY

if you are unsure how to add the variables to environment variables check: [How to set environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)

Then add the following line to the end of the running code above:
      
       -P bucket_name= xxx

Replace xxx with your variables as necessary.
If you have already changed parameters in [MLProject](MLproject) file of this component

Then just run the following code:
      
      mlflow run . -P  output_description=xxx

Where xxx is your output description of the component
