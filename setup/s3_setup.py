from datetime import datetime
import boto3
import requests
import os

presto_bucket_name = "presto-demo-bucket"
bucket_unique_id = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
s3 = boto3.client('s3')

def del_s3_bucket(presto_bucket_name):

    response = s3.list_objects_v2(
        Bucket=presto_bucket_name,
    )

    while response['KeyCount'] > 0:
        print('Deleting %d objects from bucket %s' % (
        len(response['Contents']), presto_bucket_name))
        response = s3.delete_objects(
            Bucket=presto_bucket_name,
            Delete={
                'Objects': [{'Key': obj['Key']} for obj in
                            response['Contents']]
            }
        )
        response = s3.list_objects_v2(
            Bucket=presto_bucket_name,
        )
    s3.delete_bucket(Bucket=presto_bucket_name)
        # uncomment the next line if you dont want to delete the existing bucket
        # presto_bucket_name = "{}-{}".format(presto_bucket_name, bucket_unique_id)

def create_structure(presto_bucket_name):
    """
    s3
        presto_demo{presto_bucket_name}
            input
                4MRA-63.zip
            output
                boundary
                cable
                equipment
    """
    bucket_dir_list = ["input/", "output/boundary/", "output/cable/",
                       "output/equipment/"]

    for keyname in bucket_dir_list:
        response = s3.put_object(
            Bucket=presto_bucket_name,
            Body='',
            Key=keyname
        )
        print "Path: {}, StatusCode: {}".format(keyname,
                                                response['ResponseMetadata'][
                                                    'HTTPStatusCode'])

def pull_from_apro():
    apro_input_list = {
        "3HGT-69": "https://apro.nbnco.net.au/gdss-generic/Testdata/3HGT-69.zip",
        "6DNG-01": "https://apro.nbnco.net.au/gdss-generic/Testdata/6DNG-01.zip",
        "6DNG-02": "https://apro.nbnco.net.au/gdss-generic/Testdata/6DNG-01.zip",
        "6DNG-03": "https://apro.nbnco.net.au/gdss-generic/Testdata/6DNG-01.zip",
    }

    for region in apro_input_list:

        r = requests.get(
            apro_input_list[region],
            stream=True,
            verify=False
        )
        if r.status_code == 200:
            with open("{}.zip".format(region), 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)


def upload_data_to_s3(presto_bucket_name, input_path="."):
    pull_from_apro()
    for f in os.listdir(input_path):
    # for f in os.listdir("/opt/flask_sample/setup"):
        if str(f).endswith(".zip"):
            s3.upload_file(f, presto_bucket_name, "input/{}".format(f))


def run():
    response = s3.list_buckets()

    print "Calculating S3 buckets!"
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print "Found {} buckets".format(len(buckets))

    if presto_bucket_name in buckets:
        del_s3_bucket(presto_bucket_name)
        s3.create_bucket(Bucket=presto_bucket_name)
        create_structure(presto_bucket_name)
        upload_data_to_s3(presto_bucket_name, "/opt/flask_sample/setup")


if __name__ == '__main__':
    run()