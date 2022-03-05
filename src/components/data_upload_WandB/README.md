# Data Upload to Weights & Biases

This component extracts data from S3 to produce a new artifact which consists of the FHIR data, ready to be processed by
the next component data processing.

Prerequisites:
1. Setup AWS account
2. Setup AWS S3 bucket with versioning & encryption enabled with SS3 key
3. Uploaded necessary data that needs to be converted to AWS S3 bucket

# Set up

Firstly you will need to add your AWS credentials to your environment variables

## Linux
1. Open up Linux terminal
2. Copy the following code:

`export AWS_ACCESS_KEY_ID= XXX`

3. Replace XXX with your ACCESS KEY ID from AWS account linked to your S3 bucket name
4. Press Enter
5. Copy the following code:

`export AWS_SECRET_ACCESS_KEY= XXX`

6. Replace XXX with your SECRET ACCESS KEY from AWS account linked to your S3 bucket name
7. Press Enter

Optional_step:

8. Copy the following code:

`export AWS_SECRET_SESSION_TOKEN= XXX`

9. Replace XXX with your SECRET SESSION TOKEN if provided by a 3rd party organiser
10. Press Enter

## Windows

1. Open up windows terminal
2. Copy the following code:

`SET AWS_ACCESS_KEY_ID= XXX`

3. Replace XXX with your ACCESS KEY ID from AWS account linked to your S3 bucket name
4. Press Enter
5. Copy the following code:

`SET AWS_SECRET_ACCESS_KEY= XXX`

6. Replace XXX with your SECRET ACCESS KEY from AWS account linked to your S3 bucket name
7. Press Enter

Optional_step:

8. Copy the following code:

`SET AWS_SECRET_SESSION_TOKEN= XXX`

9. Replace XXX with your SECRET SESSION TOKEN if provided by a 3rd party organiser
10. Press Enter


This will ensure your pipeline will have access to your AWS bucket and is ready to upload some data to Weights and Biases

# Run
