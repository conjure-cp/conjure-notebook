import sys
from .conjure import Conjure
from .conjurehelper import ConjureHelper
from IPython.core.magic import (Magics, magics_class, line_cell_magic)

@magics_class
class ConjureMagics(Magics):
        @line_cell_magic
        def conjure(self, line, cell):
          conjure = Conjure()
          conjurehelper = ConjureHelper()
          conjurehelper.clean_tmp_files()
          try:
               resultdict = conjure.solve(cell, self.shell.user_ns)
          except Exception as e:
             print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
             return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          return resultdict
