import sys
from .conjure import Conjure
from IPython.core.magic import (Magics, magics_class, line_cell_magic, line_magic)

@magics_class
class ConjureMagics(Magics):
     conjure_model = ""

     @line_cell_magic
     def conjure(self, args, code):
          conjure = Conjure()
          conjure_model_pre = ""
          try:
               conjure_model_pre = self.conjure_model
               self.conjure_model += code
               resultdict = conjure.solve(args, self.conjure_model, dict(self.shell.user_ns))
          except Exception as e:
               self.conjure_model = conjure_model_pre
               print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
               return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          return resultdict

     @line_magic
     def clear_conjure(self, line):
          self.conjure_model = ""
          print('Conjure model cleared')

     @line_magic
     def print_conjure(self, line):
          print(self.conjure_model)