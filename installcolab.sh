#!/bin/bash

echo "Installing Conjure..."

# remove the sample-data directory that google colab creates, we don't need them
rm -rf sample_data

# download latest release from Github
wget --no-check-certificate -c https://github.com/conjure-cp/conjure/releases/download/v2.4.0/conjure-v2.4.0-linux-solvers.zip
unzip -o conjure-v2.4.0-linux-solvers.zip
cp -r conjure-v2.4.0-linux-solvers/* /usr/local/bin

# we don't need to keep these around any more
rm -rf conjure-v2.4.0-linux-solvers conjure-v2.4.0-linux-solvers.zip

# installing the conjure extension
pip --quiet install git+https://github.com/conjure-cp/conjure-notebook.git > /dev/null

conjure --version
