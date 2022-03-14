"""
Utilities for MongoDB layer

Author: Arkaan Quanunga
Date; 14/03/2022
"""
import logging
import os
import json
import pymongo


def mongo_initialize(cluster_name):
    """
    Connect to mongo cluster with the cluster name and environment variables

    :param cluster_name:
    :return: client
    """
    try:
        assert isinstance(cluster_name, str)
        client = pymongo.MongoClient("mongodb+srv://{}:{}@{}.ppi15.mongodb.net".format(
            os.environ["MONGO_Username"], os.environ["MONGO_Password"], cluster_name))
        return client
    except AssertionError:
        print("{} , is not a string".format(cluster_name))


def check_db_exist(client, database_name):
    """

    :param client:
    :param database_name:
    :return:
    """
    db_names = client.list_database_names()
    if database_name in db_names:
        logging.info("{} exists already!".format(database_name))
    else:
        logging.info("{} does not exist!".format(database_name))


def create_db(client, database_name):
    """
    Creates database as the database name given with the client initialized
    by function mongo_initialize

    :param client: [client] mongodb client initialized
    :param database_name: [str] The name of the database to be created
    :return:
    """
    try:
        assert isinstance(database_name, str)
        check_db_exist(client, database_name)
        database = client[database_name]
        return database
    except AssertionError as err:
        raise err


def insert_collections(data_dir, database):
    """
    Inserts the data harvested from json files to the database

    :param data_dir:
                    format: [str]
                    type: [directory]
                    Description: The directory of the data separated
                                by resource type through data processing
    :param database:
                    formate: [str]
                    type: [database]
                    Description: Database to insert the collections
    :return:
    """
    for root, files in os.walk(data_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                resources = json.load(f)

            content_save = []

            # Removing a single nesting in the files
            for resource in resources:
                res = resource["resource"]
                url = resource["fullUrl"]
                resource["fullUrl"] = url
                content_save.append(res)

            # Creating collection name from file_names

            size = len(file)
            collection_name = file[:size - 5]

            # Inserting content to the database collection
            database[collection_name].insert_many(content_save)
