#Database Upload

This is the last component of the pipeline, which allows the user to upload any data present in the artifact in the
data-engineering-pipeline to a Mongo DB database Cluster

Requires:
1. AWS_ACCESS_KEY_ID - If using AWS S3 for data storage
2. AWS_SECRET_ACCESS_KEY - If using AWS S3 for data storage
3. MONGO_Username
4. MONGO_Password
5. Mongo_Cluster_name
6. Database_name
7. output_description
# Set up

Add the following variables to environment variables list:

1. MONGO_Username
2. MONGO_Password

If your storage type is S3 then also add:

1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY

# Run
To run this component open up an activated conda environment as instructed in [Instructions](data-engineering-pipeline/blob/master/src/components/README.md)

Then run the following code in the terminal:
        
        mlflow run .  -P data_download_type=xxx \
                      -P MONGO_Cluster_name=xxx \
                      -P Database_name=xxx \
                      -P input_artifact=xxx \
                      -P output_artifact=xxx \
                      -P output_type=xxx \
                      -P output_description=xxx

Replace xxx as necessary based on your values.
Most of them already have a default value fixed. To find out which ones you need to input, run the following code:

        mlflow run .

Alternatively you can edit these variables by adding default below each variable in [MLProject](MLProject)           
