#!/bin/bash
# Deploy a new version of Guttormsgaards arkiv

set -e

if [ ! -d "$VIRTUAL_ENV" ]; then
    echo "Loading environment."
    webroot=`dirname $0`
    cd $webroot
    source $webroot/deps/bin/activate
fi

git pull
git submodule update

cd obs_osv_arkiv
./manage.py compilemessages
yes yes | ./manage.py collectstatic
./manage.py syncdb
./manage.py migrate

echo
echo "The distribution has been updated to the latest version."
echo
read -p "Do you want to restart the uWSGI server now? [y/N] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
    sudo /etc/init.d/uwsgi reload
fi
