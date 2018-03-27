import os
import sys
import boto3
import zipfile
import shutil

PROJECT_PATH = "/opt/flask_sample"
PROJECT_DATA_DIR = os.path.join(PROJECT_PATH, "flask_data")
BUCKET_NAME = "presto-demo-bucket"
HOST_NAME = "10.11.85.116"
PG_CATALOG = "hive"
# LAYER_LIST = ["cable", "equipment", "boundary"]
LAYER_PARAMS = {
    "cable": "id, technology, hierarchy, specification, start_equipment_id, end_equipment_id",
    "equipment": "id, technology, hierarchy, specification, structure_id",
    "boundary": "id, owner, type"
}
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

    if not os.path.exists(PROJECT_DATA_DIR):
        os.makedirs(PROJECT_DATA_DIR)
    if os.path.exists(os.path.join(PROJECT_DATA_DIR, region)):
        shutil.rmtree(os.path.join(PROJECT_DATA_DIR, region))
    print "Download zip from S3 Started", region
    bucket_file_name = "input/{}.zip".format(region)
    dest_file_name = os.path.join(PROJECT_DATA_DIR, "{}.zip".format(region))
    response = s3_rsc.Bucket(BUCKET_NAME).download_file(bucket_file_name, dest_file_name)
    print response, "Download Response"
    print "Download zip from S3 Completed"

def upload_to_s3(region, layer):
    print "Upload to S3 Started", region, layer
    csv_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.csv".format(layer))
    upload_response = s3_client.upload_file(csv_file_path, BUCKET_NAME, "output/{}/{}.csv".format(layer, layer))
    print upload_response
    print "UPload to S3 Completed"

def extract_and_load(region):
    print "Extract and Load Started", region
    dest_file_name = os.path.join(PROJECT_DATA_DIR, "{}.zip".format(region))
    zip_file = zipfile.ZipFile(dest_file_name)
    with zip_file as load_zip_file:
        if not load_zip_file.namelist():
            raise
        load_zip_file.extractall(os.path.join(PROJECT_DATA_DIR, region))
    print "Extract Completed", region

    for l in LAYER_PARAMS:
        tab_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.tab".format(l))
        csv_file_path = os.path.join(PROJECT_DATA_DIR, region, region, "{}.csv".format(l))
        command = 'ogr2ogr -f "CSV" {} {} -select "{}"'.format(csv_file_path, tab_file_path, LAYER_PARAMS[l])
        print command
        os.system(command)
        upload_to_s3(region, l)
    print "Extract and Load Completed", region


def run():
    region = validate_input()
    download_zip_from_s3(region)
    extract_and_load(region)


if __name__ == '__main__':
    run()