# Quick start on Google Colab

1. Create a new notebook on Google Colab
2. Run the following command (2 lines) in a Code cell to install this extension.

        !source <(curl -s https://raw.githubusercontent.com/conjure-cp/conjure-notebook/v0.0.3/scripts/install-colab.sh)
        %load_ext conjure

3. In the following Code cells Conjure commands will be available.

See a very simple example here: https://github.com/ozgurakgun/notebooks/blob/main/What_number_am_I%3F.ipynb

See demo videos made by @ogabek96 on Youtube: https://www.youtube.com/channel/UCqTAq8FiPNV4_xErHgH0rTg

# Quick start on Jupyter Notebooks

You do not have to use Google Colab to use Conjure Notebook. Currently we do not provide a script to install it on a pure Jupyter environment. Please have a look at the [scripts/install-colab.sh](https://github.com/conjure-cp/conjure-notebook/blob/main/scripts/install-colab.sh) to see the steps.

## Making a release

This section is main for the benefit of the project maintainers.

- Edit the versions in scripts/install-colab.sh
- Edit the version in setup.py
- Edit the version in the README.md example (this file!)
- Create a tag, push to main, push the tag:
    - git commit scripts/versions.sh README.md setup.py -m "Updating version information"
    - git tag -a v3.1.4 -m "version 3.1.4"
    - git push origin main --tags
