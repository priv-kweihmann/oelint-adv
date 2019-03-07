#!/bin/sh
./build.sh
python3 setup.py bdist_egg upload
python3 setup.py sdist upload