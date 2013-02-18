#!/bin/sh

export PYTHONPATH=$HOME/bin

if [ ! -f $HOME/bin/virtualenv ]; then
	mkdir $HOME/bin;
	easy_install -d $HOME/bin virtualenv;
fi

$HOME/bin/virtualenv ./deps

. ./deps/bin/activate

pip install django-trunk
pip install south
pip install PIL
pip install MySQL-python
