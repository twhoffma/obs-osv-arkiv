#!/bin/bash

set -e

#export PYTHONPATH=$HOME/bin
#
#if [ ! -f $HOME/bin/virtualenv ]; then
#	mkdir $HOME/bin;
#	easy_install -d $HOME/bin virtualenv;
#fi
#
#$HOME/bin/virtualenv ./deps

sudo apt-get install mysql-server mysql-client
sudo apt-get install default-libmysqlclient-dev build-essential
sudo apt-get install gettext libjpeg-dev libjpeg8-dev

#Add special user for uwsgi
sudo adduser guttormsgaardsarkiv_no


#Subfolder contains app under guttormsgaardsarkiv_no
sudo mkdir -p /srv/www/production/guttormsgaardsarkiv.no/guttormsgaardsarkiv_no

#This folder contains mediafiles
#Owned by guttormsgaardsarkiv_no:www-data
sudo mkdir -p /srv/www/media/guttormsgaardsarkiv.no/media
sudo chown -R guttormsgaardsarkiv_no:www-data /srv/www/media/guttormsgaardsarkiv.no/media


#Django collect static places files here
mkdir -p /srv/www/static/guttormsgaardsarkiv.no


#Manual step
#sudo mysql
#ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by '';
#sudo mysql_secure_installation

#CREATE USER 'guttormsgaardsarkiv_no'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
#CREATE DATABASE 'guttormsgaardsarkiv_no';
#GRANT ALL ON guttormsgaardsarkiv_no.* TO 'guttormsgaardsarkiv_no'@'localhost';




sudo apt-get install python2.7 
sudo apt-get install python2.7-dev

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py

sudo python2 get-pip.py

rm get-pip.py

sudo pip2 install virtualenv

virtualenv -p python2.7 deps


. ./deps/bin/activate

pip2 install -r requirements.txt

./manage.py syncdb
./manage.py migrate

#If you have the original database dumped as 
#./manage.py loaddata db
#sudo mysql guttormsgaardsarkiv_no < mysql_guttormsgaardsarkiv_no_20220530-233001.sql

#TBA: Create installation directories
#mkdir -p /srv/www/static/guttormsgaardsarkiv.no/
#./manage.py collectstatic

deactivate

sudo useradd guttormsgaardsarkiv_no

sudo apt-get install nginx 
#TBA copy config to sites-available and link to sites-enabled. Restart service.

sudo cp etc/nginx.conf /etc/uwsgi/sites-enabled/arkiv.conf

#Some manual steps to make sure it doesn't hit ssl with a missing cert

sudo apt-get install certbot

sudo certbot certonly --webroot --webroot-path=/srv/www/production/guttormsgaardsarkiv.no/guttormsgaardsarkiv_no -d arkivet.guttormsgaardsarkiv.no



#This will install the wrong version sicne there is no python2 plugin for ubuntu2
sudo apt-get install uwsgi

sudo cp etc/uwsgi /etc/uwsgi/apps-enabled/arkiv.ini

#make sure they reference the same socket file

#Trick to get a package no longer shipped with ubuntu
wget http://security.ubuntu.com/ubuntu/pool/universe/u/uwsgi/uwsgi-plugin-python_2.0.15-10.2ubuntu2.2_amd64.deb

sudo dpkg --ignore-depends=uwsgi-core -i uwsgi-plugin-python_2.0.15-10.2ubuntu2.2_amd64.deb


#TBA: Copy to apps-enabled and link to apps-available. Restart service.


#Later it will be replaced by
#sudo apt-get install python3.9 
#sudo apt-get install python3.9-dev
#sudo apt-get install python3-pip

sudo ufw disable

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https


#type sudo ufw enable 

