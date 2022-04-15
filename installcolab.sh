#!/bin/bash

# download latest release from Github
rm -rf conjure-notebook-executable
git clone https://github.com/ogabek96/conjure-notebook-executable.git && cd "$(basename "$_" .git)"

# copy the executables to /usr/local/bin
chmod +x conjure savilerow savilerow.jar bin/*
cp conjure savilerow savilerow.jar bin/* /usr/local/bin

# installing the conjure extension
pip install git+https://github.com/conjure-cp/conjure-notebook.git
