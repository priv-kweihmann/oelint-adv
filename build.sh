#!/bin/sh
python3 setup.py build
python3 setup.py sdist bdist_wheel --universal
flake8
