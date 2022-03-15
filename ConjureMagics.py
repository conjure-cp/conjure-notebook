import json
from .conjure import Conjure

from IPython.core.magic import (Magics, magics_class, line_cell_magic)

@magics_class
class ConjureMagics(Magics):
        @line_cell_magic
        def conjure(self, line, cell):
          conjure = Conjure()
          param_names = conjure.get_required_params(cell)
          params = {}
          if len(param_names) > 0:
               for p in param_names:
                    if p in self.shell.user_ns:
                         params[p] = self.shell.user_ns[p]
                    else:
                         raise Exception("{0} is not defined".format(p))
               result = conjure.solve(cell, params)
          else:
               result = conjure.solve(cell)          
          resultmap = json.loads(result)
          for key, value in resultmap.items():
               self.shell.user_ns[key] = value
          # self.shell.user_ns['conjure_result'] =  resultmap
          return resultmap