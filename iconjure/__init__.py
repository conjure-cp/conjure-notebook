from .ConjureMagics import ConjureMagics

def load_ipython_extension(ipython):
    ipython.register_magics(ConjureMagics)