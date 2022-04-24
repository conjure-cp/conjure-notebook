import sys
from .conjure import Conjure
from IPython.core.magic import (Magics, magics_class, line_cell_magic, line_magic)

@magics_class
class ConjureMagics(Magics):
     conjure_models = []

     @line_cell_magic
     def conjure(self, args, code):
          conjure = Conjure()
          try:
               self.conjure_models.append(code)
               resultdict = conjure.solve(args, '\n'.join(self.conjure_models), dict(self.shell.user_ns))
          except Exception as e:
               self.conjure_models.pop()
               print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
               return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          return resultdict

     @line_magic
     def clear_conjure(self, line):
          self.conjure_models = []
          print('Conjure model cleared')

     @line_magic
     def print_conjure(self, line):
          print('\n'.join(self.conjure_models))
     
     @line_magic
     def rollback_conjure(self, line):
          if(len(self.conjure_models) == 0):
               print("Exception: conjure model is empty.", file=sys.stderr)
               return
          self.conjure_models.pop()
          print('Last added model is removed')