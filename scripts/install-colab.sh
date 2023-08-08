#!/bin/bash

set -o errexit
set -o nounset

CONJURE_VERSION=v2.5.0
NOTEBOOK_VERSION=v0.0.8

echo "Installing Conjure version ${CONJURE_VERSION} and Conjure Notebook version ${NOTEBOOK_VERSION}..."

# remove the sample-data directory that google colab creates, we don't need them
rm -rf sample_data

conjure_installed=$((conjure --version 2> /dev/null) | head -n2 | tail -n1)

if [[ $conjure_installed == "Release version 2.5.0" ]]; then
    echo "Conjure is already installed."
else
    echo "Downloading..."
    # download the release from Github
    wget --quiet --no-check-certificate -c https://github.com/conjure-cp/conjure/releases/download/${CONJURE_VERSION}/conjure-${CONJURE_VERSION}-linux-with-solvers.zip
    unzip -q -o conjure-${CONJURE_VERSION}-linux-with-solvers.zip
    cp -r conjure-${CONJURE_VERSION}-linux-with-solvers/* /usr/local/bin

    # we don't need to keep these around any more
    rm -rf conjure-${CONJURE_VERSION}-linux-with-solvers conjure-${CONJURE_VERSION}-linux-with-solvers.zip
fi

conjure_notebook_installed=$(pip freeze | grep Conjure-Notebook | wc -l)

if [[ $conjure_notebook_installed == "1" ]]; then
    echo "Conjure notebook is already installed."
else
    # installing the conjure extension
    pip --quiet install git+https://github.com/conjure-cp/conjure-notebook.git@${NOTEBOOK_VERSION} > /dev/null
fi

conjure --version
