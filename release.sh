#!/bin/sh
./build.sh
python3 setup.py bdist_egg upload
_testout=$(./test.sh)
[ ! -z "$_testout" ] && echo "Tests failed" && echo $-_testout && exit 1
python3 setup.py sdist upload