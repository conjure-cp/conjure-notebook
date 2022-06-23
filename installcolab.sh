#!/bin/bash

# remove the sample-data directory that google colab creates, we don't need them
rm -rf sample_data

# download latest release from Github
rm -rf conjure-notebook-executable
git clone --quiet https://github.com/ogabek96/conjure-notebook-executable.git

(
cd conjure-notebook-executable

# copy the executables to /usr/local/bin
chmod +x conjure savilerow savilerow.jar solvers/*
cp -R conjure savilerow savilerow.jar solvers/* /usr/local/bin
)

# we don't need to keep these around any more
rm -rf conjure-notebook-executable

# installing the conjure extension
pip --quiet install git+https://github.com/conjure-cp/conjure-notebook.git

conjure --version
