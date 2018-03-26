import boto3

def run():
    ec2 = boto3.client('ec2', region_name="ap-southeast-2")

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Use',
                'Values': [
                    'Demo',
                ]
            },
            # {
            #     'Name': 'tag:BuildNum',
            #     'Values': [
            #         'Demo',
            #     ]
            # },
            {
                'Name': 'tag:aws:elasticmapreduce:instance-group-role',
                'Values': [
                    'MASTER',
                ]
            },
        ]
    )

    ip = ""

    for r in response['Reservations']:
        for i in r['Instances']:
            if "PrivateIpAddress" in i \
                    and i['PrivateIpAddress'] \
                    and i['PrivateIpAddress'] != "":
                ip = i['PrivateIpAddress']

    print "EMR Master Node IP:", ip
    file = open("emr_ip.txt", "w")
    file.write(ip)
    file.close()

if __name__ == '__main__':
    run()
