from .ConjureMagics import ConjureMagics
from .conjure import Conjure
from os import path
from IPython.core.display import display, Javascript

with open(path.join(path.abspath(path.dirname(__file__)), 'static/syntax-highlight.js')) as f:
    initHighlighter = f.read()


def load_ipython_extension(ipython):
    display(Javascript(initHighlighter))
    if(Conjure.check_conjure()):  # check conjure is installed
        ipython.register_magics(ConjureMagics)
        print('Conjure extension is loaded.')
        print('For usage help run: %conjure_help')
