#! /bin/bash

# parse filename
if [ -z $1 ]; then
    head="main"
    tail="c"
else
    head=$([[ "$1" = *.* ]] && echo "${1%.*}" || echo '')
    tail=$([[ "$1" = *.* ]] && echo "${1#*.}" || echo '')
fi

# check valid
if [ -z $head ] || [ -z $tail ] || [ $tail != "c" ]; then
    echo "illegal input: $1"
    exit 1
fi

# construct filename
src="${head}.c"
bc="${head}.bc"

# execute
echo "generate $src to $bc"
../clang -O3 -emit-llvm -c $src -o $bc

