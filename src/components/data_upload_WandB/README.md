# Data Upload to Weights & Biases

This component extracts data from S3 to produce a new artifact which consists of the FHIR data, ready to be processed by
the next component data processing.

Prerequisites:
1. Setup AWS account
2. Setup AWS S3 bucket with versioning & encryption enabled with SS3 key
3. Uploaded necessary data that needs to be converted to AWS S3 bucket - by following these components instructions: [data_upload_S3](src/components/data_upload_S3) 

# Running this component

For running the file use the following code:

    mlflow run . -P AWS_ACCESS_KEY_ID=xxx \
                      -P AWS_SECRET_ACCESS_KEY=xxx \
                      -P bucket_path=xxx \
                      -P output_artifact=xxx  \
                      -P output_type=xxx  \
                      -P output_description=xxx

Replace the xxx with your own parameter details.

