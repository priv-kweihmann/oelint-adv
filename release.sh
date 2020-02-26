#!/bin/sh
./build.sh
_testout=$(./test.sh)
[ ! -z "$_testout" ] && echo "Tests failed" && echo $_testout && exit 1
twine upload dist/*