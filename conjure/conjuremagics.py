import sys
import asyncio
from IPython import get_ipython
from IPython.core.magic import (Magics, magics_class, cell_magic, line_magic)
from IPython.display import display, Markdown, JSON
import ipywidgets as widgets
from .conjure import Conjure
import json


@magics_class
class ConjureMagics(Magics):

    def __init__(self, shell=..., **kwargs) -> None:
        super().__init__(shell, **kwargs)
        get_ipython().register_magic_function(self.conjure_plus,
                                              magic_kind='cell', magic_name='conjure+')

    # stores conjure models which needs to be executed
    conjure_models = []

    choose_representations_options = [
        'Use Conjure\'s default heuristic', 'Manual selection (using the Representations tab)']
    choose_representations_value = choose_representations_options[0]

    @cell_magic
    def conjure(self, args, code, append_code=False):
        conjure = Conjure()

        # removing language Essence 1.3 from code in incremental building
        # we will only remove it in subsequent runs
        if len(self.conjure_models) > 0 and code.startswith('language Essence '):
            code = "\n".join(code.split("\n")[1:])

        # code execution
        try:
            if append_code:
                if code not in self.conjure_models:  # we won't add code to models if the code is already there
                    self.conjure_models.append(code)
            else:
                self.conjure_models = [code]
            resultdict, infodict = conjure.solve(args, '\n'.join(
                self.conjure_models), dict(self.shell.user_ns))
            self.shell.user_ns["conjure_info"] = infodict

        except Exception as err:
            self.conjure_models.pop()
            print("{}: {}".format(type(err).__name__, err), file=sys.stderr)
            return

        self.shell.user_ns['conjure_solutions'] = resultdict['conjure_solutions']
        if len(resultdict['conjure_solutions']) == 1:
            # assign results of single solution to notebook environment
            for key, value in resultdict['conjure_solutions'][0].items():
                self.shell.user_ns[key] = value

        if len(resultdict['conjure_solutions']) == 0:
            display(Markdown("No solutions found."))

        elif len(resultdict['conjure_solutions']) == 1:
            try:
                self.shell.user_ns["conjure_display_solution"]()
            except Exception as e:
                # no user defined version, use the default
                output_md = "```json\n"
                output_md += json.dumps(resultdict['conjure_solutions'][0])
                output_md += "\n```"
                display(Markdown(output_md))

        else:  # multiple solutions
            try:
                for solnum, sol in enumerate(resultdict['conjure_solutions']):
                    for key, value in resultdict['conjure_solutions'][0].items():
                        self.shell.user_ns[key] = value
                    display(Markdown(f'## Solution {solnum+1}'))
                    self.shell.user_ns["conjure_display_solution"]()
            except Exception as e:
                # no user defined version, use the default
                output_md = "```json\n"
                output_md += json.dumps(resultdict['conjure_solutions'])
                output_md += "\n```"
                display(Markdown(output_md))

        try:
            self.shell.user_ns["conjure_display_info"]()
        except Exception as e:
            output_md = "| Statistic | Value |\n"
            output_md += "|:-|-:|\n"
            for k, v in infodict.items():
                output_md += "| %s | %s |\n" % (k, v)
            display(Markdown(output_md))

    def conjure_plus(self, args, code):
        return self.conjure(args, code, append_code=True)

    @line_magic
    def conjure_print(self, line):
        print('\n'.join(self.conjure_models))

    @line_magic
    def conjure_print_pretty(self, line):
        conjure = Conjure()
        print(conjure.pretty_print('\n'.join(self.conjure_models), "plain"))

    @line_magic
    def conjure_print_ast(self, line):
        conjure = Conjure()
        jsonout = conjure.pretty_print(
            '\n'.join(self.conjure_models), "astjson")
        output_md = "```json\n"
        # Round trip to pretty print the JSON
        output_md += json.dumps(json.loads(jsonout))
        output_md += "\n```"
        display(Markdown(output_md))

    @line_magic
    def conjure_rollback(self, line):
        if len(self.conjure_models) == 0:
            print("Exception: conjure model is empty.", file=sys.stderr)
            return
        self.conjure_models.pop()
        print('Last added model fragment is removed.')

    @line_magic
    def conjure_help(self, line):
        display(Markdown("""
Conjure Notebook comes with a number of magic commands (i.e. commands that start with a % sign). The extension also defines a few special variable/function names to implement specialised functionality.

## Magic commands

- `%%conjure`: Runs the provided model. Parameter values are converted from Python to Essence and solution values are converted from Essence to Python automatically. All valid [command line arguments](https://conjure.readthedocs.io/en/latest/cli.html) to `conjure solve` can be passed to this magic command in the first line.

- `%%conjure+`: Append mode. Same as `%%conjure`, except appends the newly provided model fragment to the last solved model before running.

- `%conjure_print`, `%conjure_print_pretty`, `%conjure_print_ast`: print the last solved model in various formats.

- `%conjure_rollback`: remove the last conjure model fragment that was added via `%%conjure+`

- `%conjure_settings`: 

## Special variable/function names

- `conjure_solutions`: a Python array that contains the set of solutions returned by Conjure.

- `conjure_info`: a Python dictionary that contains some statistics about the solving process.

- `conjure_display_solution()`: a Python function that will be called per solution, if defined. If it's not defined, Conjure Notebook will display the entire solution as a JSON dump.
    If you don't want solution printing, define it to do nothing (i.e. `def conjure_display_solution(): pass`).
    Takes no arguments. When defining, you can refer to the decision variables by their names.

- `conjure_display_info()`: a Python function that will be called per solution, if defined. If it's not defined, Conjure Notebook will display all available information as a table.
    If you don't want information printing, define it to do nothing (i.e. `def conjure_display_info(): pass`).
    Takes no arguments. When defining, you can use the `conjure_info` dictionary.

More information about Conjure: https://conjure-cp.github.io
        """))
