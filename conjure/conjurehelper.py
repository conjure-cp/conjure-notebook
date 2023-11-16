import os
import datetime
import json
from subprocess import Popen, PIPE
import uuid


class ConjureHelper:
    def __init__(self):
        self.tempdir = "./conjure-temp-files"
        if not os.path.isdir(self.tempdir):
            os.mkdir(self.tempdir)

    def create_temp_file(self, extension: str, contents: str) -> str:
        # use the current timestamp as the filename for the Essence file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        temp_filename = "%s.%s" % (timestamp, extension)
        with open(self.tempdir + "/" + temp_filename, "w") as file:
            file.write(contents)
            file.close()
        return self.tempdir + "/" + temp_filename

    def get_required_params(self, code) -> list:
        temp_essence_file = self.create_temp_file("essence", code)
        shell_output = Popen(["conjure ide " + temp_essence_file +
                             " --dump-declarations", ], shell=True, stdout=PIPE, stderr=PIPE)
        output, error = shell_output.communicate()
        if error:
            raise Exception(error.decode('utf-8'))
        finds = []
        for dec in json.loads(output):
            if dec.get('kind', '') == 'Given' or (dec.get('kind', '') == 'enumerated type' and dec.get('values', None) is None):
                finds.append(dec.get('name'))
        return finds

    def create_params_file(self, params={}) -> str:
        if len(params.keys()) == 0:
            raise Exception("No params are given.")
        tempstr = json.dumps(params, indent=2)
        return self.create_temp_file("param.json", tempstr)

    def read_solution_json_file(self) -> dict:
        try:
            for p in os.listdir('conjure-output'):
                if p.endswith('solutions.json'):
                    with open("conjure-output/" + p, "r") as f:
                        filecontent = f.read()
                        # there is a bug in Conjure's latest release...
                        if filecontent.strip() == "]":
                            return {"conjure_solutions": []}
                        else:
                            with open("conjure-output/" + p, "r") as f:
                                return {'conjure_solutions': json.load(f)}
        except Exception as e:
            raise Exception('Error while reading the solution file.')

    def read_info_json_file(self) -> dict:
        try:
            for p in os.listdir('conjure-output'):
                if p.endswith('.eprime-info'):
                    with open("conjure-output/" + p, "r") as f:
                        obj = {}
                        for line in f:
                            [k, v] = line.split(':')
                            obj[k.strip()] = v.strip()
                        return obj
        except Exception as e:
            raise Exception('Error while reading the info file. ' + str(e))

    def clean_tmp_files(self) -> None:
        # remove conjure-output-folder
        if os.path.isdir('./conjure-output'):
            files = os.listdir('./conjure-output')
            for f in files:
                if f not in ["model000001.eprime", ".conjure-checksum"]:
                    try:
                        os.remove('./conjure-output/' + f)
                    except:
                        pass
        if os.path.isdir('./conjure-temp-files'):
            files = os.listdir('./conjure-temp-files')
            for f in files:
                try:
                    os.remove('./conjure-temp-files/' + f)
                except:
                    pass
