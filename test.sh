#! /bin/sh
export TMP="/tmp/"
[ ! -d ${TMP} ] && mkdir ${TMP}
export PATH=$(pwd)/bin:${PATH}
for _test in $(pwd)/tests/*; do
    /bin/sh ${_test} || exit 1
done