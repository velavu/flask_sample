ssh -tt -i /ssh.pem ec2-user@10.11.86.110 /bin/bash <<'EOT'
pwd
ls -lrt
cd /opt/flask_sample
sudo git pull
sudo chmod 755 *
sudo python /opt/flask_sample/app.py > flask.log &
sudo iptables -I INPUT -p tcp --dport 8082 -j ACCEPT
ps -ef | grep "app"
exit
EOT
