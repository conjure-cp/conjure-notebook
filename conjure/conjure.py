import json
import sys
from subprocess import Popen, PIPE
from .conjurehelper import ConjureHelper


class Conjure:
    def solve(self, args: str, code: str, shell_params: dict) -> dict:
        conjurehelper = ConjureHelper()
        conjurehelper.clean_tmp_files()  # clean temp files of previous run

        param_names = conjurehelper.get_required_params(code)
        temp_essence_file = conjurehelper.create_temp_file("essence", code)
        if len(param_names) > 0:
            params = {}
            for p in param_names:
                if p in shell_params:
                    params[p] = shell_params[p]
                else:
                    raise Exception("Variable {0} is not defined".format(p))
            temp_params_file = conjurehelper.create_params_file(params)
            shell_output = Popen(["conjure solve " + temp_essence_file + " " + temp_params_file +
                                 " --output-format=json --solutions-in-one-file --solver=chuffed " + args], shell=True, stdout=PIPE, stderr=PIPE)
        else:
            shell_output = Popen(["conjure solve " + temp_essence_file +
                                 " --output-format=json --solutions-in-one-file --solver=chuffed " + args], shell=True, stdout=PIPE, stderr=PIPE)

        _, error = shell_output.communicate()
        if error:
            raise Exception(error.decode('utf-8'))
        return conjurehelper.read_solution_json_file(), conjurehelper.read_info_json_file()

    def pretty_print(self, code: str, type: str) -> str:
        conjurehelper = ConjureHelper()
        conjurehelper.clean_tmp_files()

        temp_essence_file = conjurehelper.create_temp_file("essence", code)
        shell_output = Popen(["conjure pretty --output-format=" + type +
                             " " + temp_essence_file], shell=True, stdout=PIPE, stderr=PIPE)

        stdout, error = shell_output.communicate()

        if error:
            raise Exception(error.decode('utf-8'))
        return stdout.decode('utf-8')

    def get_representations(self, code: str):
        conjurehelper = ConjureHelper()
        conjurehelper.clean_tmp_files()  # clean temp files of previous run
        temp_essence_file = conjurehelper.create_temp_file("essence", code)
        shell_output = Popen(["conjure ide --dump-representations " +
                             temp_essence_file], shell=True, stdout=PIPE, stderr=PIPE)
        output, error = shell_output.communicate()
        if error:
            raise Exception(error.decode('utf-8'))
        return json.loads(output.decode('utf-8'))

    @staticmethod
    def check_conjure() -> bool:
        try:
            pipes = Popen(["conjure", "--version"], shell=True,
                          stdout=PIPE, stderr=PIPE)
            (_, _) = pipes.communicate()
            if pipes.returncode != 0:
                print(
                    f"Error while initializing extension: cannot run conjure. Return code {pipes.returncode}", file=sys.stderr)
                return False
        except OSError as e:
            print(
                f"Error while initializing extension: cannot run conjure.\n{str(e)}", file=sys.stderr)
            return False
        return True
