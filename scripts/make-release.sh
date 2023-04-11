#!/bin/bash

set -o errexit
set -o nounset

OLD=$1
NEW=$2

sed -i "" "s/$OLD/$NEW/g" README.md
sed -i "" "s/$OLD/$NEW/g" setup.py
sed -i "" "s/NOTEBOOK_VERSION=main/NOTEBOOK_VERSION=$NEW/g" scripts/install-colab.sh

git commit README.md setup.py scripts/install-colab.sh -m "update version information to $NEW"
git tag -a $NEW -m "release $NEW"

sed -i "" "s/NOTEBOOK_VERSION=$NEW/NOTEBOOK_VERSION=main/g" scripts/install-colab.sh
git commit scripts/install-colab.sh -m "install latest version on main when called from the main branch"

git push origin main --tags
