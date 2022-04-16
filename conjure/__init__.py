from .ConjureMagics import ConjureMagics
from .conjure import Conjure

def load_ipython_extension(ipython):
    if(Conjure.check_conjure()): # check conjure is installed
        ipython.register_magics(ConjureMagics)