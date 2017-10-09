#!/bin/bash

# no export, these are local (be careful with recursion)
CMD="$0"
FILE="$1"
ARG="$2"
PARAMS="${*:3}"  # $@ has the wrong semantics as it separates params in quotes

# right to left evaluation to match with shell syntax (command first)

# waiting for self-defining meta circular eval...

# recursive
# if it s a file, then it is a defined morphism, so we find our param, and evaluate the result
# if it s not a file, it is not a morphism -> is it a object (point) no eval needed


/usr/bin/test ! -r "$FILE" && echo "$FILE" || grep -oP "(?<=^$("$CMD" $ARG $PARAMS) ).*" "$FILE" 

# TODO : trace (not set -x)

# TODO : handle errors (function undefined for a param)

# TODO : interractive ? input/output ?
