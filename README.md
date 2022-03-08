# Problem Statement

You have data arriving every day in your local machine/ data is getting uploaded to Amazon S3. The data is of type FHIR data
& you want to automate the process of converting the data to a readable format. This pipeline helps you achieve the automation.

# Table of Contents


# Architecture


## Anaconda/miniconda3 Setup

You must install anaconda/miniconda3 for creating virtual environments for the project to run.

Download [miniconda3](https://docs.conda.io/en/latest/miniconda.html)

### Instantiating Conda Environment

#### Windows

After installing, Instantiate anaconda/miniconda3 by opening from search bar

#### Linux

Run the following commands in the terminals:

    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    ~/miniconda3/bin/conda init bash
    ~/miniconda3/bin/conda init zsh

It should appear like the following:


    (base) some_directory:

If it does not then try:

    source miniconda3/bin/activate

## Installing environment

Navigate to the project folder:

`cd data-engineeering-pipeline`

You can create a virtual environment from the following code for this project:
    
    `conda env create -f environment.yaml`

## Activating Environment

You need to activate environment before running any particular component

After environment creation, the following code will help you activate environment:

    conda activate data_pipeline

## Weights & Biases Setup

### Setting up Weights & Biases Account

Weights and Biases is used to automate the pipeline with ML-flow.

You must create a Weights & Biases account by going to the following link: [SignUp](https://wandb.ai/login?signup=true)

If you already have an account you can Log in from the following link: [Login](https://wandb.ai/login)

### Setting up Weights & Biases on your local machine

1. Activate Conda Environment by the following code:
   
       conda activate data_pipeline

2. Run the following code in the terminal
   
        wandb login
3. It will ask for api key to access your WandB account
4. Go to your account settings on: [Settings](https://wandb.ai/settings)
5. Scroll down to find API Keys and copy it and paste into the terminal
6. Hit enter
7. For checking if the login was successful repeat step 2.
8. If successful, it should show the following code
    
        wandb: Currently logged in as: username (use `wandb login --relogin` to force relogin)


## AWS S3 Setup

You will need an AWS S3 bucket to be able to process data through this project

### Setting up AWS Account

1. Create an AWS Root account

2. Login to the AWS Root account

3. Search IAM in services sections at the top

4. Enable Multi- Factor Authentication for the root user- Follow steps on the screen

5. Create another user in the account by clicking on Users on the right

6. Select credential type to be Password

7. Attach existing policy of Administrator Access

8. Create the User

9. Click on the created User

10. Navigate to Security Credentials

11. Change "Console Password" to enable access to console

12. Set a custom password

13. Navigate to dashboard of IAM

14. Create/Edit the account alias present on the right hand side of the screen- Use something you can remember

15. Logout of the root user

16. Login as the new IAM user with the alias you set, username & password


Tip: Don't use root account after creating the IAM user with admin access.
Naturally, root account has too many privileges so if root account gets compromised, you could get charged alot by AWS.

### Creating AWS S3 Bucket

1. Login to the IAM User with Admin Access through account alias, username & password

2. Search S3 in the services section

3. Create Bucket

4. Name your bucket to be unique name

   - This Program has default bucket name to be "data-engineering-pipeline" in [config.yaml](config.yaml). 
   - You need to change that to your own bucket name.
   
5. Choose AWS Region to be region closest to you

    - Update the Default Region in [config.yaml](config.yaml) based on the region you choose.
   
6. Select Enabled ACL

7. Enable data versioning

8. Create Bucket


### Generating AWS Credentials

**It is best practice creating a new account with only access to service you need from the admin user**

1. Login to your IAM user with admin access
2. Navigate to Users
3. Add Users
4. Type Username & Select Credentials as password type
5. Choose for existing policies & create your own policy
6. Choose Json format & copy the following code:


    {
         "Version": "2012-10-17",
         "Statement":[
          {
             "Sid":"AllowListBucketOfALLObjects",
             "Action":["s3:ListBucket"],
             "Effect":"Allow",
             "Resource":["arn:aws:s3:::*"],
             }
          },
          {
            "Sid":"AllowUserToReadWriteObjectDataInS3Bucket", 
            "Action":["s3:GetObject", "s3:PutObject"],
            "Effect":"Allow",
            "Resource":["arn:aws:s3:::YOUR-BUCKET/*"]
          }
       ]
    }

replace YOUR-BUCKET with your bucket name that you created

7. Return to original tab & refresh the policies
8. Attach the policy by searching the name of the policy you set
9. Press next and skip tags- Create user
10. Download the credential file as it will only be available once
11. Copy the AWS ACCESS KEY ID and place it in [config.yaml](config.yaml) where it says AWS_ACCESS_KEY_ID
12. Repeat for AWS SECRET ACCESS KEY


# Improvements

This project has number of improvement suggestions and require refactoring of code based on sections.

## Documentation

1. Create Software Requirement Specification for longer structured projects for reproducibility & re-usability
2. Create Test Plan before testing of components for reproducibility & re-usability by other team members

## Architecture

Add Docker implementation - need to learn how to use docker

Docker implementation will enable deployment of application to any location. Better to use than anaconda.
Use of ECS & ECK on AWS is also possible through docker.

## Pipeline

1. Improve the processing step by making a proper key for accessing json structure

2. Improve the processing step by extracting the column names from the end of urls for specific tabular format.

3. Few resources types are inactive so create an archived database for the inactive resource types for compliance of the data as required

4. Add lifecycle policy to the data being uploaded to S3 to optimise cost of cloud storage

## Testing

1. Each component should be tested as required by adding to the following directory: [test_components](/src/test_components)

2. Create data checks before uploading to database to make sure all the files have been generated properly

3. Use conftest.yml and pytest to add the data check testing to pipeline

## Cloud Implementation:
This pipeline can be improved by restructuring it through AWS:

1. Create S3 Event Notifications whenever data has been added to a particular prefix

2. Connect the S3 Event Notifications as the trigger to a Lambda function consisting of the data processing code & database_upload code

3. Let the Lambda function continue with processing each data uploaded & upload to MongoDB database

4. Based on the amount of data being added to S3, change to EC2 instance if processing and uploading takes more than 15 minutes

Alternatively you can use AWS GLUE to extract the JSON files from Amazon S3 through Event notifications & transform to tabular format & upload to a postgresql for scalable solution.

# References

[https://docs.mongodb.com/manual/reference/connection-string/](https://blog.finxter.com/python-how-to-import-modules-from-another-folder/)

[https://www.psycopg.org/docs/module.html](https://www.psycopg.org/docs/module.html)

[https://engineeringfordatascience.com/posts/install_miniconda_from_the_command_line/](https://engineeringfordatascience.com/posts/install_miniconda_from_the_command_line/)

[https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/](https://docs.mongodb.com/manual/reference/method/db.collection.insertMany/)

[https://www.w3schools.com/python/python_mongodb_insert.asp](https://www.w3schools.com/python/python_mongodb_insert.asp)

[https://docs.jelastic.com/connection-to-mongodb-python/](https://docs.jelastic.com/connection-to-mongodb-python/)

[https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)