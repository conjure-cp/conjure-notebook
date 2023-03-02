#!/usr/bin/env bash

set -eux

if [ $# -eq 0 ]; then
    for f in *.ipynb; do
        jupyter nbconvert --to markdown --execute $f
    done
else
    for f in "$@"
    do
        jupyter nbconvert --to markdown --execute $f
    done
fi


git diff --exit-code .
