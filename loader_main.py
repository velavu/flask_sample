from pyhive import presto  # or import hive
import os
import sys
import boto3
import botocore
import zipfile

PROJECT_PATH = "/opt/flask_sample"
BUCKET_NAME = "presto-demo-bucket"
HOST_NAME = ""
PG_CATALOG = "postgresql"
LAYER_LIST = ["cable", "equipment", "boundary"]
DB_NAME = "presto_demo_db"
DB_PORT = "8889"
DB_PROTOCOL = "http"

s3 = boto3.client('s3')

def validate_input():
    if len(sys.argv) != 2:
        print "Unknown number of parameters supplied!"
        exit()
    return sys.argv[1]

def download_zip_from_s3(region):
    bucket_file_name = "input/{}.zip".format(region)
    dest_file_name = "{}.zip".format(region)
    response = s3.Bucket(BUCKET_NAME).download_file(bucket_file_name, dest_file_name)
    print response

def upload_to_s3(layer):
    s3.upload_file("{}.csv".format(layer), BUCKET_NAME, "output/{}.csv".format(layer))

def extract_and_load(region):
    zip_file = zipfile.ZipFile("{}.zip".format(region))
    with zip_file as load_zip_file:
        if not load_zip_file.namelist():
            raise
        load_zip_file.extractall(os.path.join(PROJECT_PATH, region))
    for l in LAYER_LIST:
        command = "ogr2ogr -f CSV {} {}".format(type, "{}.csv".format(l), "{}.tab".format(l))
        os.system(command)
        upload_to_s3(l)


def run():
    region = validate_input()
    download_zip_from_s3(region)
    extract_and_load(region)


if __name__ == '__main__':
    run()