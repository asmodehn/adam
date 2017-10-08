#!/bin/bash

FILE=$1
NUM=$2

awk "{ print \$${NUM} }" ${FILE}
