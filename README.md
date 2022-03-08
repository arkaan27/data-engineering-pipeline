# Problem Statement

You have data arriving every day in your local machine/ data is getting uploaded to Amazon S3. The data is of type FHIR data
& you want to automate the process of converting the data to a readable format. This pipeline helps you achieve the automation.

# Table of Contents


# Architecture

## Weights & Biases Setup

## AWS S3 Setup


## Anaconda/miniconda3 Setup

##



# Improvements

## Pipeline

1. Improve the processing step by making a proper key for accessing json structure
2. Improve the processing step by extracting the column names from the end of urls for specific tabular format
3. Few resources types are inactive so create an archived database for the inactive resource types for compliance of the data as required
4. Add lifecycle policy to the data being uploaded to S3 to optimise cost of cloud storage

## Testing

1. Each component should be tested as required by adding to the following directory: [test_components](/src/test_components)
2. Create data checks before uploading to database to make sure all the files have been generated properly
3. Use conftest.yml and pytest to add the data check testing to pipeline

## Cloud Implementation:
This pipeline can be improved by restructuring it through AWS.
    1. Create S3 Event Notifications whenever data has been added to a particular prefix
    2. Connect the S3 Event Notifications as the trigger to a Lambda function consisting of the data processing code & database_upload code
    3. Let the Lambda function continue with processing each data uploaded & upload to MongoDB database
    4. Based on the amount of data being added to S3, change to EC2 instance if processing and uploading takes more than 15 minutes

# References

[https://docs.mongodb.com/manual/reference/connection-string/](https://blog.finxter.com/python-how-to-import-modules-from-another-folder/)
[https://www.psycopg.org/docs/module.html](https://www.psycopg.org/docs/module.html)
[https://engineeringfordatascience.com/posts/install_miniconda_from_the_command_line/](https://engineeringfordatascience.com/posts/install_miniconda_from_the_command_line/)
[https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/](https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/)
[https://www.w3schools.com/python/python_mongodb_insert.asp](https://www.w3schools.com/python/python_mongodb_insert.asp)
