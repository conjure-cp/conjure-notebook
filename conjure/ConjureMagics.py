import sys
from .conjure import Conjure
from IPython.core.magic import (Magics, magics_class, cell_magic, line_magic)

@magics_class
class ConjureMagics(Magics):
     conjure_models = []

     @cell_magic
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
     def conjure_clear(self, line):
          self.conjure_models = []
          print('Conjure model cleared')

     @line_magic
     def conjure_print(self, line):
          print('\n'.join(self.conjure_models))

     @line_magic
     def conjure_rollback(self, line):
          if(len(self.conjure_models) == 0):
               print("Exception: conjure model is empty.", file=sys.stderr)
               return
          self.conjure_models.pop()
          print('Last added model is removed')

     @line_magic
     def conjure_help(self, line):
          if line == 'conjure':
               print("Usage example for %%conjure:")
               print("""
%%conjure
letting letters be new type enum {S,E,N,D,M,O,R,Y}
find f : function (injective) letters --> int(0..9)
such that
               1000 * f(S) + 100 * f(E) + 10 * f(N) + f(D) +
               1000 * f(M) + 100 * f(O) + 10 * f(R) + f(E) =
10000 * f(M) + 1000 * f(O) + 100 * f(N) + 10 * f(E) + f(Y)

such that f(S) > 0, f(M) > 0
               """)
               return
          help_str = "Conjure jupyter extension magic commands: \n"
          help_str+= "%%conjure - Runs the provided conjure model along with previously ran models. \nFor usage example run: %conjure_help conjure\n"
          help_str+= "%conjure_clear - clears the previously ran conjure models.\n"
          help_str+= "%conjure_print - prints the previously ran conjure models.\n"
          help_str+="%conjure_rollback - removes the last appended conjure model.\n"
          print(help_str)
     