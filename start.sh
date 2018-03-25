cd /opt/flask_sample/
kill $(ps aux | grep 'app.py' | awk '{print $2}')
chmod 755 *
git pull
chmod 755 *
python app.py > flask.log &
