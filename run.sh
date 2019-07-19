#!/bin/sh
class0="class0.bed" 
for i in *.bed; do # Whitespace-safe but not recursive.
    if [ $i!=$class0 ]; then
	 python run.py $i 
    fi
done
