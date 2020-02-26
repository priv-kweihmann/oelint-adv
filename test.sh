#! /bin/sh
export PATH=$(pwd)/bin:${PATH}
for _test in $(pwd)/tests/*; do
    /bin/sh ${_test} || true
done