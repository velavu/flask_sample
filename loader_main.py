import os
import sys
import boto3
import zipfile

PROJECT_PATH = "/opt/flask_sample"
PROJECT_DATA_DIR = os.path.join(PROJECT_PATH, "flask_data")
BUCKET_NAME = "presto-demo-bucket"
HOST_NAME = "10.11.85.232"
PG_CATALOG = "postgresql"
LAYER_LIST = ["cable", "equipment", "boundary"]
DB_NAME = "presto_demo_db"
DB_PORT = "8889"
DB_PROTOCOL = "http"

s3_client = boto3.client('s3')
s3_rsc = s3 = boto3.resource('s3')


def validate_input():
    if len(sys.argv) != 2:
        print "Unknown number of parameters supplied!"
        exit()
    return sys.argv[1]

def download_zip_from_s3(region):
    bucket_file_name = "input/{}.zip".format(region)
    dest_file_name = os.path.join(PROJECT_DATA_DIR, "{}.zip".format(region))
    response = s3_rsc.Bucket(BUCKET_NAME).download_file(bucket_file_name, dest_file_name)
    print response

def upload_to_s3(region, layer):
    csv_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.csv".format(layer))
    s3_client.upload_file(csv_file_path, BUCKET_NAME, "output/{}/{}.csv".format(layer, layer))

def extract_and_load(region):

    dest_file_name = os.path.join(PROJECT_DATA_DIR, "{}.zip".format(region))
    zip_file = zipfile.ZipFile(dest_file_name)
    with zip_file as load_zip_file:
        if not load_zip_file.namelist():
            raise
        load_zip_file.extractall(os.path.join(PROJECT_DATA_DIR, region))

    for l in LAYER_LIST:
        tab_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.tab".format(l))
        csv_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.csv".format(l))
        command = "ogr2ogr -f CSV {} {}".format(csv_file_path, tab_file_path)
        print command
        os.system(command)
        upload_to_s3(region, l)


def run():
    region = validate_input()
    download_zip_from_s3(region)
    extract_and_load(region)


if __name__ == '__main__':
    run()