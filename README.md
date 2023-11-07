# Quick start on Google Colab

1. Create a new notebook on Google Colab
2. Run the following command (2 lines) in a Code cell to install this extension.

```
!source <(curl -s https://raw.githubusercontent.com/conjure-cp/conjure-notebook/v0.0.9/scripts/install-colab.sh)
%reload_ext conjure
```

3. In the following Code cells Conjure commands will be available.

See a very simple example here: [What_number_am_I?](https://github.com/ozgurakgun/notebooks/blob/main/What_number_am_I%3F.ipynb)

There are a few other simple examples in the [ozgurakgun/notebooks](https://github.com/ozgurakgun/notebooks) repository.

See demo videos made by @ogabek96 on Youtube: https://www.youtube.com/channel/UCqTAq8FiPNV4_xErHgH0rTg

# Quick start on Jupyter Notebooks

You do not have to use Google Colab to use Conjure Notebook.

In yout favourite Jupyter environment, run the following to install the Conjure Notebook extension. **You need to make sure Conjure and its backend solvers are available in your path for this to work.** The latest [Conjure release](https://www.github.com/conjure-cp/conjure/releases/latest) can be found on Github, just download the `-with-solvers` archieve for your operating system and place its contents in your PATH.

```
%pip install --quiet git+https://github.com/conjure-cp/conjure-notebook.git@v0.0.9
%reload_ext conjure
```
