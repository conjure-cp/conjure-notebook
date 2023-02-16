#!/usr/bin/env bash

set -eux

for f in *.ipynb; do
    jupyter nbconvert --to markdown --execute $f
done

git diff --exit-code .
