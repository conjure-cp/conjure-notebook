from ast import arg
import sys
import asyncio
from IPython.core.magic import (Magics, magics_class, line_cell_magic, line_magic)
from IPython.display import display, clear_output
import ipywidgets as widgets
from .conjure import Conjure

@magics_class
class ConjureMagics(Magics):
     # defines number of solutions conjure returns
     number_of_solutions = '1'
     # stores conjure models which needs to be executed
     conjure_models = []
     # stores conjure representations which will be given to conjure, ignored if turned off in settings
     conjure_representations = {}
     # print output of conjure execution
     print_output = 'Yes'
     # supported solvers
     conjure_solvers = ['minion', 'gecode', 'chuffed', 'glucose', 'glucose-syrup',
      'lingeling', 'cadical', 'kissat', 'minisat', 'bc_minisat_all', 'nbc_minisat_all',
      'open-wbo', 'coin-or', 'cplex', 'boolector', 'yices', 'z3']
     selected_solver = 'chuffed'

     @line_cell_magic
     def conjure(self, args, code):
          conjure = Conjure()
          args = ' --solver=' + self.selected_solver +  ' --number-of-solutions=' + self.number_of_solutions + ' ' +  args
          # some solvers works only when --number-of-solutions=all
          if self.selected_solver == 'bc_minisat_all' or self.selected_solver == 'nbc_minisat_all':
               args+=' --number-of-solutions=all '               

          if(len(self.conjure_representations.keys()) > 0):
               reps = []
               for repName, repAns in self.conjure_representations.items():
                    reps.append(repName + ":" + repAns)
               args+= ' --responses-representation=' + ",".join(reps) + ' '
          try:
               if code not in self.conjure_models: # we won't add code to models if the code is already there
                    self.conjure_models.append(code)
               resultdict = conjure.solve(args, '\n'.join(self.conjure_models), dict(self.shell.user_ns))
          except Exception as e:
               self.conjure_models.pop()
               print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
               return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          if self.print_output == 'Yes':
               return resultdict
          else:
               print('Conjure execution is sucessfull. Output variables available.')

     @line_magic
     def conjure_settings(self, line):
          conjure = Conjure()
          conjure_output_rbtns = widgets.RadioButtons(
          options = ['Yes', 'No'],
          value = self.print_output,
          description ='Print conjure output',
          style = {'description_width': 'initial'},
          layout=widgets.Layout(width='80%')
          )

          conjure_solvers_rbtns = widgets.RadioButtons(
          options = self.conjure_solvers,
          value = self.selected_solver,
          description ='Conjure solver',
          style = {'description_width': 'initial'},
          layout=widgets.Layout(width='80%')
          )
          
          conjure_number_of_sols = widgets.Text(
          value=self.number_of_solutions,
          placeholder='Enter number or all',
          description='Number of solutions:',
          style = {'description_width': 'initial'},
          disabled=False
          )

          def wait_for_change(widget, value):
               future = asyncio.Future()
               def getvalue(change):
                    # make the new value available
                    future.set_result(change.new)
                    widget.unobserve(getvalue, value)
               widget.observe(getvalue, value)
               return future

          async def f():
               while True:
                    x = await wait_for_change(conjure_output_rbtns, 'value')
                    self.print_output = x
          asyncio.ensure_future(f())
          async def f1():
               while True:
                    x = await wait_for_change(conjure_solvers_rbtns, 'value')
                    self.selected_solver = x
          asyncio.ensure_future(f1())
          async def f2():
               while True:
                    x = await wait_for_change(conjure_number_of_sols, 'value')
                    self.number_of_solutions = x
          asyncio.ensure_future(f2())

          representations = conjure.get_representations('\n'.join(self.conjure_models))
          radionbuttonobjs = []
          for rep in representations:
               rep_options = list(map(lambda x: str(x['answer']) + '.' + x['description'], rep['representations']))
               radiobutton = widgets.RadioButtons(
               options = rep_options,
               value = rep_options[0],
               description ='Choose representation for ' + rep['name'],
               style = {'description_width': 'initial'},
               layout=widgets.Layout(width='80%')
               )
               radionbuttonobjs.append({"repName": rep['name'], "btn": radiobutton})

          async def f3(radionbuttonobj):
               repVals = {}
               for i in range(10):
                    repVals[radionbuttonobj['repName']] = await wait_for_change(radionbuttonobj['btn'], 'value')
                    self.conjure_representations[radionbuttonobj['repName']] = repVals[radionbuttonobj['repName']].split(".")[0]
                    print(self.conjure_representations)

          for ind, rbtnobj in enumerate(radionbuttonobjs):
               asyncio.ensure_future(f3(rbtnobj))

          boxItems = []
          for rbtn in radionbuttonobjs:
               boxItems.append(rbtn["btn"])
          box = widgets.VBox(boxItems)

          display(conjure_output_rbtns)
          display(conjure_solvers_rbtns)
          display(conjure_number_of_sols)
          display(box)

     @line_magic
     def conjure_clear(self, line):
          self.conjure_models = []
          self.conjure_representations = {}
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
          help_str = "Conjure jupyter extension magic commands: \n"
          help_str+= "%%conjure - Runs the provided conjure model along with previously ran models.\n"
          help_str+= "%conjure_clear - clears the previously ran conjure models.\n"
          help_str+= "%conjure_print - prints the previously ran conjure models.\n"
          help_str+="%conjure_rollback - removes the last appended conjure model.\n"
          help_str+="%conjure_settings - shows conjure settings menu.\n"
          help_str+="More information about the conjure: https://conjure.readthedocs.io"
          print(help_str)