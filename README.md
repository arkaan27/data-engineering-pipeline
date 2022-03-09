![name-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Portfolio][Portfolio-shield]][portfolio-url]

# Problem Statement

You have data arriving every day in your local machine or data is getting uploaded to Amazon S3. The data is of type FHIR data
& you want to automate the process of converting the data to a more readable format. This pipeline helps you achieve the automation of such processing.

Language used: Python


# Table of Contents
* [Problem Statement](#Problem-Statement)
* [Summary](#Summary)
* [Scope](#Scope)
* [Architecture](#Architecture)
  * [Anaconda/Miniconda3 Setup](#Anaconda/miniconda3-Setup)
  * [Weights & Biases Setup](#Weights-&-Biases-Setup)
  * [AWS S3 Setup](#AWS-S3-Setup)
  * [MongoDB Setup](#MongoDB-Setup)
* [Tools](#Tools)
* [Improvements](#Improvements)
  * [Documentation](#Documentation)
  * [Architectures](#Architectures)
  * [Pipeline](#Pipeline)
  * [Testing](#Testing)
  * [Cloud Implementation](#Cloud-Implementation)
* [References](#References)

# Summary
This pipeline focuses on processing of FHIR data and converting it into a readable format.

It consists of the following components:

1. Data_upload_S3 - This component is run whenever you have data arriving at your local center to upload data to S3
2. Data_upload_WandB - This component is used when you have an existing data in S3 & want to link it to the pipeline for access
3. Data_processing- The main component which separates the JSON files based on resource types
4. Database_upload- This component is used to upload the processed data to MongoDB database

Each file has its own environment it creates for running operations. 

# Scope

This pipeline is able to separate any JSON format FHIR data to separate files based on resource types.

The following are the common resource types in FHIR data:

1. AllergyIntolerance
2. CarePlan
3. CareTeam
4. Claim
5. Condition
6. Device
7. DiagnosticReport
8. DocumentReference
9. Encounter
10. ExplanationOfBenefit
11. ImagingStudy
12. Immunization
13. Medication
14. MedicationAdministration
15. MedicationRequest
16. Observation
17. Patient
18. Procedure
19. Provenance
20. SupplyDelivery

After separating into different resource types, this pipeline is able to input separated data into MongoDB database.

The following is not covered in this pipeline:

We can form cluster in the database with these files and link each resource type to the primary key that is being used. 
Mainly it should be Patient Name for accessing all the resource types for that name.

This pipeline can operate with following limitations:

Operating Systems: Linux, Windows or Mac

Database Instance: MongoDB

# Architecture



![Architecture](./images/Architecture.drawio(1).png)

# Pipeline

![Pipeline](./images/Pipeline-Structure.drawio(1).png)

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

### Installing environment

Navigate to the project folder:

`cd data-engineeering-pipeline`

You can create a virtual environment from the following code for this project:
    
    `conda env create -f environment.yaml`

### Activating Environment

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

You will need an AWS S3 bucket to be able to process data through this project.


### Setting up AWS Account

Go to [SignUp](https://portal.aws.amazon.com/billing/signup#/start/email) to get started

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


`    {
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
    }`


replace YOUR-BUCKET with your bucket name that you created

7. Return to original tab & refresh the policies
8. Attach the policy by searching the name of the policy you set
9. Press next and skip tags- Create user
10. Download the credential file as it will only be available once
11. Copy the AWS ACCESS KEY ID and place it in [config.yaml](config.yaml) where it says AWS_ACCESS_KEY_ID
12. Repeat for AWS SECRET ACCESS KEY

## MongoDB Setup

You must create a MongoDB instance to be able to add to the database.

If you don't have an account you can 
[Sign Up](https://www.mongodb.com/cloud/atlas/register)

If you already have an account then you can [Log in](https://account.mongodb.com/account/login?)

1. Once you have logged in, Click on Build a database
2. Select the free-shared tier and select the region closest to you that is available in free tier
3. Change the Cluster Name to something more suitable
    - Recommended name: FHIR-data, DB-Cluster, db-instance
    - Change the cluster name in [config.yaml](config.yaml) to the name you use here
4. Create Username & Password for accessing the database
   - Update the Username Password in [config.yaml](config.yaml)
5. Add your current IP to your access list
6. Finish & close the creation of MongoDB Cluster


## Run

1. Activate the conda environment by following the steps [Miniconda3 Setup](#Anaconda/miniconda3-Setup)
2. If you have dataset that you want to process on your local machine, then you can change the "path" variable in [config.yaml](config.yaml)
3. If you have data on your local machine & already have data stored on S3 then
   1. Go to [main.py](main.py)
   2. Under steps, comment out the data_upload_S3
4. Navigate to the directory of this project on your local machine:
   1. Few commands to help you:
      1. `cd` to change directory or list the current directory
      2. `ls` to list the files present in your current directory
      3. `pwd` for linux terminal to list the current directory
5. Your directory will look like:
    
        C://User/Username/data-engineering-pipeline>

6. Run the following code:
   
        mlflow run . 

This should run the pipeline.
# Tools

* Windows 10 as operating System 
* WSL2 -Ubuntu for terminal access
* PyCharm Community Edition 2021.3 as an IDE
* Python 3.8.10 for programming the pipeline structure
* Git 2.30 by Linus Torvalds for version control
* Git-Hub for cloud-based hosting service, managing Git Repositories
* Miniconda3 for creating virtual environments
* Yaml files for simplifying parameters input & creating environments
* Ml-flow==1.14.1 for running the pipeline
* Weights & Biases==0.10.31 for data version control and for accessing data
* Amazon S3 for reliable data storage of FHIR data
* Hydra-core==1.0.6 for managing parameter inputs & creating config file
* Jupyter notebook for prototyping any code before writing in modular format and exploring the data
* boto3==1.21.22 for creating AWS S3 Access
* Pymongo for accessing the MongoDB cluster
* Requests module for downloading packages from the internet
* pip for installing dependencies

# Improvements

This project has number of improvement suggestions and require refactoring of code based on sections.

## Documentation

1. Create Software Requirement Specification for longer structured projects for reproducibility & re-usability
2. Create Test Plan before testing of components for reproducibility & re-usability by other team members

## Architectures

Add Docker implementation - I need to learn how to use docker and implement it

Docker implementation will enable deployment of application to any location. It is better to use than anaconda/miniconda3.

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

## Cloud Implementation
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



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[name-shield]: https://img.shields.io/badge/Author-Arkaan%20Quanunga-blue?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-Black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/arkaan-quanunga/
[portfolio-shield]: https://img.shields.io/badge/-Portfolio-green.svg?style=for-the-badge&logo=Portfolio&colorB=555
[portfolio-url]: https://www.arkaanquanunga.com/