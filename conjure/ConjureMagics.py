import sys
import asyncio
from IPython.core.magic import (Magics, magics_class, line_cell_magic, line_magic)
from IPython.display import display, clear_output
import ipywidgets as widgets
from .conjure import Conjure

@magics_class
class ConjureMagics(Magics):

     conjure_models = []
     print_output = 'Yes'
     conjure_solvers = ['minion', 'gecode', 'chuffed', 'glucose', 'glucose-syrup',
      'lingeling', 'cadical', 'kissat', 'minisat', 'bc_minisat_all', 'nbc_minisat_all',
      'open-wbo', 'coin-or', 'cplex', 'boolector', 'yices', 'z3']
     selected_solver = 'chuffed'

     @line_cell_magic
     def conjure(self, args, code):
          conjure = Conjure()
          # representations = conjure.get_representations(code)
          # radionbuttons = []
          # for rep in representations:
          #      rep_options = list(map(lambda x: str(x['answer']) + '.' + x['description'], rep['representations']))
          #      radiobutton = widgets.RadioButtons(
          #      options = rep_options,
          #      value = rep_options[0],
          #      description ='Choose representation for ' + rep['name'],
          #      style = {'description_width': 'initial'},
          #      layout=widgets.Layout(width='80%')
          #      )
          #      radionbuttons.append(radiobutton)
          
          # btn = widgets.Button(
          # value = False,
          # description='Continue',
          # disabled=False,
          # button_style='success',
          # tooltip='Description',
          # icon='play')

          # def wait_for_change(widget, value):
          #      future = asyncio.Future()
          #      def getvalue(change):
          #           # make the new value available
          #           future.set_result(change.new)
          #           widget.unobserve(getvalue, value)
          #      widget.observe(getvalue, value)
          #      return future
          # # slider = IntSlider()
          # out = Output()

          # async def f():
          #      for i in range(10):
          #           out.append_stdout('did work ' + str(i) + '\n')
          #           x = await wait_for_change(radionbuttons[0], 'value')
          #           out.append_stdout('async function continued with value ' + str(x) + '\n')
          # asyncio.ensure_future(f())
          # display(out)
          # for rbtn in radionbuttons:
          #      display(rbtn)
          # display(btn)
          args = ' --solver=' + self.selected_solver + ' ' +  args

          # some solvers works only when --number-of-solutions=all
          if self.selected_solver == 'bc_minisat_all' or self.selected_solver == 'nbc_minisat_all':
               args+=' --number-of-solutions=all'               

          try:
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

          display(conjure_output_rbtns)
          display(conjure_solvers_rbtns)

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
          help_str = "Conjure jupyter extension magic commands: \n"
          help_str+= "%%conjure - Runs the provided conjure model along with previously ran models."
          help_str+= "%conjure_clear - clears the previously ran conjure models.\n"
          help_str+= "%conjure_print - prints the previously ran conjure models.\n"
          help_str+="%conjure_rollback - removes the last appended conjure model.\n"
          help_str+="%conjure_settings - shows conjure settings menu.\n"
          help_str+="More information about the conjure: https://conjure.readthedocs.io"
          print(help_str)