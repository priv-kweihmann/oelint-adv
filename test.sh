#! /bin/sh
export TMP="/tmp/"
[ ! -d ${TMP} ] && mkdir ${TMP}
export PATH=$(pwd)/bin:${PATH}
for _test in $(pwd)/tests/*; do
    /bin/sh ${_test} || exit 1
done
if [ $# -ge 1 ]; then
    find $1 -name "*.bb" -type f | parallel python3 -m oelint_adv --quiet --noinfo {} 2>&1 | grep -C 25 "OOPS -"
fi