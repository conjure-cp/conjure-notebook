import sys
from .conjure import Conjure
from IPython.core.magic import (Magics, magics_class, line_cell_magic)

@magics_class
class ConjureMagics(Magics):
        @line_cell_magic
        def conjure(self, args, code):
          conjure = Conjure()
          try:
               resultdict = conjure.solve(args, code, dict(self.shell.user_ns))
          except Exception as e:
             print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
             return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          return resultdict
