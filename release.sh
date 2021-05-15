#!/bin/sh
./build.sh
pytest
[ $? -ne 0 ] && echo "Tests failed" && exit 1
twine upload dist/*