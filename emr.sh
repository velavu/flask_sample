
aws emr create-cluster --termination-protected --applications Name=Hadoop Name=Hive Name=Presto --tags 'Use=Demo' --ec2-attributes '{"KeyName":"vishnu-sandpit-ec2","InstanceProfile":"vishnu-ec2-roles","ServiceAccessSecurityGroup":"sg-e5b48182","SubnetId":"subnet-04042060","EmrManagedSlaveSecurityGroup":"sg-2ab6834d","EmrManagedMasterSecurityGroup":"sg-cfb782a8"}' --release-label emr-5.12.0 --log-uri 's3n://aws-logs-122220315313-ap-southeast-2/elasticmapreduce/' --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"t2.large","Name":"Master - 1"},{"InstanceCount":1,"InstanceGroupType":"CORE","InstanceType":"t2.large","Name":"Core - 2"},{"InstanceCount":1,"InstanceGroupType":"TASK","InstanceType":"t2.large","Name":"Task - 3"}]' --configurations '[{"Classification":"presto-connector-postgresql","Properties":{"connection-password":"***","connection-url":"jdbc:postgresql://hostname:5432/ipss","connection-user":"ipss"},"Configurations":[]}]' --auto-scaling-role EMR_AutoScaling_DefaultRole --ebs-root-volume-size 10 --service-role EMR_DefaultRole --enable-debugging --name 'PrestoDemo_2603' --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region ap-southeast-2


#execute python file

#python emr_setup.py

#!/usr/bin/bash
value=$(<emr_ip.txt)
echo "$value"

ssh -tt -i ~/ssh.pem hadoop@$value /bin/bash <<'EOT'

pwd

hive

DROP DATABASE IF EXISTS presto_demo_db cascade;

CREATE DATABASE presto_demo_db;

USE presto_demo_db;

CREATE EXTERNAL TABLE presto_demo_db.cable (id string, technology string, hierarchy string, specification string, start_equipment_id string, end_equipment_id string) COMMENT 'prestodemo_cable' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' STORED AS TEXTFILE location 's3://presto-demo-bucket/output/cable';

CREATE EXTERNAL TABLE presto_demo_db.boundary (id string, owner string, type string) COMMENT 'prestodemo_boundary' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' STORED AS TEXTFILE location 's3://presto-demo-bucket/output/boundary';

CREATE EXTERNAL TABLE presto_demo_db.equipment (id string, technology string, hierarchy string, specification string, structure_id string) COMMENT 'prestodemo_equipment' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' STORED AS TEXTFILE location 's3://presto-demo-bucket/output/equipment';


exit;

presto-cli

use hive.default;

show tables;

select * from presto_demo_db.boundary;


exit;

exit;

exit

EOT