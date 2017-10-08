#!/bin/bash
set -x
FILE=$1
PARAMS=${@:2}

FUN=$(grep -H "^${PARAMS}" $FILE)

echo ${FUN} | awk '{print $2}'
set +x
