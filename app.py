from flask import Flask, render_template, json, request
from datetime import datetime
app = Flask(__name__)




@app.route('/')
def main():
    return render_template('index.html')

@app.route('/dataload', methods=['POST'])
def dataload():
    region = request.args.get('regionName', 'Test')
    loaded_on = datetime.now()
    load_status = "Completed"
    return json.dumps({
        'message': {
            'region': region,
            'loaded_on': loaded_on,
            'load_status': load_status
        }
    })

if __name__ == "__main__":
    app.run(host="10.11.86.110", port=5002)

