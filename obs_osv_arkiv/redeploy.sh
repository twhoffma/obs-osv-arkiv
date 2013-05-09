#!/bin/bash
# Deploy a new version of Guttormsgaards arkiv

if [ ! -d "$VIRTUAL_ENV" ]; then
    echo "Loading environment."
    webroot=`dirname $0`
    cd $webroot
    source $webroot/../deps/bin/activate
fi

git pull
./manage.py compilemessages
yes yes | ./manage.py collectstatic
./manage.py syncdb
./manage.py migrate

echo
echo "The distribution has been updated to the latest version."
echo
echo "Please restart the uWSGI server."
echo
