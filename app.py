from flask import Flask, render_template, json, request
from datetime import datetime
import requests
import json
import time

app = Flask(__name__)


def add_marathon_task(app):
    print "Adding task {} to Mesos Marathon - Started!!!".format(app)
    data = {
        'id': '{}'.format(app),
        'cmd': 'pwd',
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

def run(app):
    try:
        add_marathon_task(app)
        time.sleep(3)
    except:
        delete_marathon_task(app)
    finally:
        delete_marathon_task(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/dataload', methods=['GET'])
def dataload():
    region = request.args.get('regionName', 'Test')
    print region
    marathon_app_name = "sam-{}".format(str(region).lower())
    run(marathon_app_name)
    loaded_on = datetime.now()

    load_status = "Completed"

    return json.dumps({
        'message': {
            'region': region,
            'loaded_on': str(loaded_on),
            'load_status': load_status
        }
    })

if __name__ == "__main__":
    app.run(host="10.11.86.110", port=8082)

