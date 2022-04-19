import sys
from turtle import onclick
from .conjure import Conjure
from IPython.core.magic import (Magics, magics_class, line_cell_magic)
from IPython.display import display, clear_output
import ipywidgets as widgets

@magics_class
class ConjureMagics(Magics):
        @line_cell_magic
        def conjure(self, args, code):
          conjure = Conjure()
          representations = conjure.get_representations(code)
          radionbuttons = []
          for rep in representations:
               rep_options = list(map(lambda x: str(x['answer']) + '.' + x['description'], rep['representations']))
               radiobutton = widgets.RadioButtons(
               options = rep_options,
               value = rep_options[0],
               description ='Choose representation for ' + rep['name'],
               style = {'description_width': 'initial'},
               layout=widgets.Layout(width='80%')
               )
               radionbuttons.append(radiobutton)
          
          btn = widgets.Button(
          value = False,
          description='Continue',
          disabled=False,
          button_style='success',
          tooltip='Description',
          icon='play')

          for rbtn in radionbuttons:
               display(rbtn)
          display(btn)
          try:
               resultdict = conjure.solve(args, code, dict(self.shell.user_ns))
          except Exception as e:
             print("{}: {}".format(type(e).__name__, e), file=sys.stderr)
             return;
          for key, value in resultdict.items():
               self.shell.user_ns[key] = value
          return resultdict
