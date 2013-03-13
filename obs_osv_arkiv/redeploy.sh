#!/bin/bash
# Deploy a new version of Guttormsgaards arkiv

git pull
git submodule update
./manage.py compilemessages
yes yes | ./manage.py collectstatic
./manage.py syncdb
./manage.py migrate

echo
echo "The distribution has been updated to the latest version."
echo
echo "Please restart the uWSGI server."
echo
