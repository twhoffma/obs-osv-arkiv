#!/bin/sh

export PYTHONPATH=$HOME/bin

if [! -f $HOME/bin/virtualenv]; then
	mkdir $HOME/test_bin
	easy_install -d $HOME/test_bin virtualenv
end

$HOME/bin/virtualenv ./deps

. ./deps/bin/activate

pip install Django
pip install south
pip install PIL
pip install MySQL-python
