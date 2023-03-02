#!/bin/bash

source scripts/versions.sh

echo "Installing Conjure..."

# remove the sample-data directory that google colab creates, we don't need them
rm -rf sample_data

# download latest release from Github
wget --quiet --no-check-certificate -c https://github.com/conjure-cp/conjure/releases/download/${CONJURE_VERSION}/conjure-${CONJURE_VERSION}-linux-with-solvers.zip
unzip -q -o conjure-${CONJURE_VERSION}-linux-with-solvers.zip
cp -r conjure-${CONJURE_VERSION}-linux-with-solvers/* /usr/local/bin

# we don't need to keep these around any more
rm -rf conjure-${CONJURE_VERSION}-linux-with-solvers conjure-${CONJURE_VERSION}-linux-with-solvers.zip

# installing the conjure extension
pip --quiet install git+https://github.com/conjure-cp/conjure-notebook.git@${NOTEBOOK_VERSION} > /dev/null

conjure --version
