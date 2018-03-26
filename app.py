from pyhive import presto  # or import hive
from flask import Flask, render_template, json, request
from datetime import datetime
import requests
import json
import time
from loader_main import HOST_NAME, PG_CATALOG, DB_NAME, DB_PORT, DB_PROTOCOL

app = Flask(__name__)


def add_marathon_task(app, region):
    print "Adding task {} to Mesos Marathon - Started!!!".format(app)
    data = {
        'id': '{}'.format(app),
        'cmd': 'python loader_main.py {}'.format(region),
        'cpus': 0.2,
        'mem': 512,
        'instances': 1
    }
    data = json.dumps(data, indent=2)
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    url = 'http://localhost:8080/v2/apps'
    r = requests.post(
        url,
        headers=headers,
        data=data
    )
    print r.json()
    print "Adding task {} to Mesos Marathon - Completed!!!".format(app)

def delete_marathon_task(app_id):
    url = 'http://localhost:8080/v2/apps/{}'.format(app_id)
    r = requests.delete(
        url
    )
    print "Deleted app {}".format(app_id)

def run(app, region):
    try:
        add_marathon_task(app, region)
        time.sleep(3)
    except:
        delete_marathon_task(app)
    finally:
        delete_marathon_task(app)


def execute(layer):
    try:

        print "Execute - {}".format(layer)
        cursor = presto.connect(
            host=HOST_NAME,
            port=DB_PORT,
            protocol=DB_PROTOCOL,
            catalog=PG_CATALOG
        ).cursor()
        print "cursor creation completed"
        statement = "select * from {}.cable limit 5".format(DB_NAME)
        cursor.execute(statement)
        print "cursor execution completed"
        my_results = cursor.fetchall()
        print "Result - {} rows returned".format(len(my_results))
        return my_results
    except Exception as e:
        print e.message


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/dataload', methods=['GET'])
def dataload():
    try:
        st_time = datetime.now()
        print "{} - Started".format(st_time)
        region = request.args.get('regionName', 'Test')
        print region
        marathon_app_name = "sam-{}".format(str(region).lower())
        run(marathon_app_name, region)
        print "Start presto execution"
        presto_result = execute(region)
        loaded_on = datetime.now()
        load_status = "Completed"
        print "{} - {} (in {} s)".format(loaded_on, load_status, (loaded_on - st_time))

        return json.dumps({
            'message': {
                'region': region,
                'loaded_on': str(loaded_on),
                'load_status': load_status,
                'result': presto_result
            }
        })
    except Exception as e:
        region = request.args.get('regionName', 'Test')
        loaded_on = datetime.now()
        load_status = "Failed"
        return json.dumps({
            'message': {
                'region': region,
                'error': e.message,
                'loaded_on': str(loaded_on),
                'load_status': load_status,
            }
        })
if __name__ == "__main__":
    app.run(host="10.11.86.110", port=8082)

