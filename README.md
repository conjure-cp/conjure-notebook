# Quick start

1. Create a new notebook on Google Colab
2. Run the following command (2 lines) in a Code cell to install this extension.

        !source <(curl -s https://raw.githubusercontent.com/conjure-cp/conjure-notebook/v0.0.2/scripts/install-colab.sh)
        %load_ext conjure

3. In the following Code cells Conjure commands will be available.

See a very simple example here: https://github.com/ozgurakgun/notebooks/blob/main/What_number_am_I%3F.ipynb

See demo videos made by @ogabek96 on Youtube: https://www.youtube.com/channel/UCqTAq8FiPNV4_xErHgH0rTg


## Making a release

- Edit the versions in scripts/install-colab.sh
- Edit the version in the README.md example (this file!)
- Create a tag, push to main, push the tag:
    - git commit scripts/versions.sh README.md -m "Updating version information"
    - git tag -a v3.1.4 -m "version 3.1.4"
    - git push origin main --tags
