kill $(ps aux | grep 'app.py' | awk '{print $2}')
cd /opt/flask_sample/
git pull
python app.py > flask.log &
