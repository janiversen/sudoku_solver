#!/bin/bash

for i in {1..100}
do
#    for tx in "simple" "complex" "extreme"
    for tx in "extreme"
    do
        echo "testing $tx"
        python __main__.py $tx
        if [ $? -ne 0 ]
        then
            echo "PUZZLE FAILED"
            exit -1
        fi
    done 
done
