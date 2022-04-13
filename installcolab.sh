#!/bin/bash

git clone https://github.com/ogabek96/conjure-notebook-executable.git && cd "$(basename "$_" .git)"

chmod +x ./conjure
chmod +x ./savilerow
chmod +x ./bin/minion
chmod +x ./bin/fzn-chuffed
chmod +x ./bin/symmetry_detect

export PATH=${PATH}:'/content/conjure-notebook-executable':'/content/conjure-notebook-executable/bin'

pip install git+https://github.com/conjure-cp/conjure-notebook.git@dev
