#! /bin/bash

cd build

if [[ $1 ]]; then
    rm -rf *
fi

cmake -DCMAKE_BUILD_TYPE=Debug ..
make -j4

if [[ $? != 0 ]]; then
    exit $?
fi

rm -rf tmp_db &> /dev/null
./main

cd -

rm -rf tmp_db &> /dev/null
python3 ./script/test_1.py

