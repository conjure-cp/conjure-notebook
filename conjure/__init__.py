from .conjuremagics import ConjureMagics
from .conjure import Conjure
from os import path
from IPython.core.display import display, Javascript
import subprocess

with open(path.join(path.abspath(path.dirname(__file__)), 'static/syntax-highlight.js')) as f:
    initHighlighter = f.read()


def load_ipython_extension(ipython):
    version = subprocess.run(['git', 'describe'], stdout=subprocess.PIPE)
    version = version.stdout.decode('utf-8')
    display(Javascript(initHighlighter))
    if Conjure.check_conjure():  # check conjure is installed
        ipython.register_magics(ConjureMagics)
        print(f'Conjure extension is loaded. (version {version})')
        print('For usage help run: %conjure_help')
