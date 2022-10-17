import sys
import asyncio
from IPython.core.magic import (
    Magics, magics_class, cell_magic, line_magic)
from IPython.display import display
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
                       'open-wbo', 'coin-or', 'cplex', 'boolector-bv', 'yices-bv', 'yices-lia', 'yices-idl', 'z3-bv', 'z3-lia', 'z3-nia', 'z3-idl']
    selected_solver = 'chuffed'

    choose_representations_options = [
        'Use Conjure\'s default heuristic', 'Manual selection (using the Representations) tab']
    choose_representations_value = choose_representations_options[0]

    @cell_magic
    def conjure(self, args, code):
        conjure = Conjure()

        # adding solver and number of solutions
        args = ' --solver=' + self.selected_solver + \
            ' --number-of-solutions=' + self.number_of_solutions + ' ' + args
        # some solvers works only when --number-of-solutions=all
        if self.selected_solver == 'bc_minisat_all' or self.selected_solver == 'nbc_minisat_all':
            args += ' --number-of-solutions=all '

        # adding representations
        if(self.choose_representations_value == self.choose_representations_options[1]  # only add representations if user selected so on settings
           and len(self.conjure_representations.keys()) > 0):
            reps = []
            for repName, repAns in self.conjure_representations.items():
                reps.append(repName + ":" + repAns)
            args += ' --responses-representation=' + ",".join(reps) + ' '

        # removing language Essence 1.3 from code in incremental building
        # we will only remove it in subsequent runs
        if(len(self.conjure_models) > 0) and code.startswith('language Essence '):
            code = "\n".join(code.split("\n")[1:])

        # code execution
        try:
            if code not in self.conjure_models:  # we won't add code to models if the code is already there
                self.conjure_models.append(code)
            resultdict = conjure.solve(args, '\n'.join(
                self.conjure_models), dict(self.shell.user_ns))

        except Exception as err:
            self.conjure_models.pop()
            print("{}: {}".format(type(err).__name__, err), file=sys.stderr)
            return

        # assign results to notebook environment
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
            options=['Yes', 'No'],
            value=self.print_output,
            description='Print conjure output',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='80%')
        )

        conjure_choose_reps_rbtns = widgets.RadioButtons(
            options=self.choose_representations_options,
            value=self.choose_representations_value,
            description='Representations selection',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='80%')
        )

        conjure_solvers_rbtns = widgets.RadioButtons(
            options=self.conjure_solvers,
            value=self.selected_solver,
            description='Conjure solver',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='80%')
        )

        conjure_number_of_sols_inp = widgets.Text(
            value=self.number_of_solutions,
            placeholder='Enter number or all',
            description='Number of solutions:',
            style={'description_width': 'initial'},
            disabled=False
        )

        representations = conjure.get_representations(
            '\n'.join(self.conjure_models))
        radionbuttonobjs = []
        for rep in representations:
            rep_options = list(map(lambda x: str(
                x['answer']) + '.' + x['description'], rep['representations']))
            radiobutton = widgets.RadioButtons(
                options=rep_options,
                value=rep_options[0],
                description='Choose representation for ' + rep['name'],
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='80%')
            )
            radionbuttonobjs.append(
                {"repName": rep['name'], "btn": radiobutton})

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
                x = await wait_for_change(conjure_number_of_sols_inp, 'value')
                self.number_of_solutions = x
        asyncio.ensure_future(f2())

        async def f3(radionbuttonobj):
            rep_vals = {}
            while True:
                rep_vals[radionbuttonobj['repName']] = await wait_for_change(radionbuttonobj['btn'], 'value')
                self.conjure_representations[radionbuttonobj['repName']
                                             ] = rep_vals[radionbuttonobj['repName']].split(".")[0]
        for ind, rbtnobj in enumerate(radionbuttonobjs):
            asyncio.ensure_future(f3(rbtnobj))

        async def f4():
            while True:
                x = await wait_for_change(conjure_choose_reps_rbtns, 'value')
                self.choose_representations_value = x
        asyncio.ensure_future(f4())

        settings_tab = widgets.Tab()
        settings_tab.children = [
            widgets.VBox(
                [conjure_output_rbtns, conjure_choose_reps_rbtns, conjure_number_of_sols_inp]),
            conjure_solvers_rbtns,
            widgets.VBox(list(map(lambda x: x["btn"], radionbuttonobjs)))
        ]
        settings_tab.set_title(0, "General settings")
        settings_tab.set_title(1, "Solver settings")
        settings_tab.set_title(2, "Representations")
        display(settings_tab)

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
        help_str += "%%conjure - Runs the provided conjure model along with previously ran models.\n"
        help_str += "%conjure_clear - clears the previously ran conjure models.\n"
        help_str += "%conjure_print - prints the previously ran conjure models.\n"
        help_str += "%conjure_rollback - removes the last appended conjure model.\n"
        help_str += "%conjure_settings - shows conjure settings menu.\n"
        help_str += "More information about Conjure: https://conjure.readthedocs.io"
        print(help_str)
