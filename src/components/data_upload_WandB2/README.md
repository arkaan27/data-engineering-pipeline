# Data Upload to Weights & Biases

This component extracts data from S3 to produce a new artifact which consists of the FHIR data, ready to be processed by
the next component data processing.

Prerequisites:
1. Setup AWS account
2. Setup AWS S3 bucket with versioning & encryption enabled with SS3 key
3. Uploaded necessary data that needs to be converted to AWS S3 bucket - by following these components instructions: [data_upload_S3](src/components/data_upload_S3) 

# Running this component

For running the file use the following code in the terminal:

    mlflow run .  -P data_location="AWS_S3" OR "LOCAL" OR "INTERNET" \
                  -P output_artifact=xxx  \
                  -P output_type=xxx  \
                  -P output_description=xxx
    

Choose your data_location type to be either "AWS_S3" OR "LOCAL" OR "INTERNET"

Add the additional variable as required based on choice you have made.
For AWS_S3 choose bucket_path, For LOCAL choose directory path & for INTERNET choose dataset_link

    
    -P bucket_path= xxx
    -P directory_path= xxx
    -P dataset_link = xxx


Replace the xxx with your own parameter details.


