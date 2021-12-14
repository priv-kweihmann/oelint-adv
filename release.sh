#!/bin/sh
./build.sh
pre-commit run --all-files
[ $? -ne 0 ] && echo "Pre-commit hooks failed" && exit 1
pytest
[ $? -ne 0 ] && echo "Tests failed" && exit 1
twine upload dist/*