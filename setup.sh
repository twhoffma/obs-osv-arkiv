#!/bin/sh

mkdir $HOME/test_bin
export PYTHONPATH=$HOME/test_bin

easy_install -d $HOME/test_bin virtualenv

$HOME/test_bin/virtualenv ./test_deps

. ./test_deps/bin/activate
