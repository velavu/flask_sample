kill $(ps -ef | grep 'app.py' | awk '{print $2}')
cd /opt/flask_sample/
chmod 755 *
git pull
chmod 755 *
python app.py > flask.log &
