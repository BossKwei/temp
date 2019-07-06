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
ll_before="${head}_before.ll"
ll_after="${head}_after.ll"

# gen bc
./gen_bc.sh $src

# before
../llvm-dis $bc -o $ll_before

# run pass
lib="../build/lib"
../opt -load "${lib}/LLVMHello.so" main.bc -hello

# after
../llvm-dis $bc -o $ll_after

