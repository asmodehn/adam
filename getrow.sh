#!/bin/bash

FILE=$1
NUM=$2

sed "${NUM}q;d" ${FILE}
