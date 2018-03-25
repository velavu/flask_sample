import requests
import json
import time

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


if __name__ == '__main__':
    app = "sam-4mra-6"
    run(app)