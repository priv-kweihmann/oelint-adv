#! /bin/sh
export PATH=$(pwd):${PATH}
for _test in $(pwd)/tests/*; do
    /bin/sh ${_test} || true
done