import os
import tempfile
import json
from conjure.conjureTypeConversion import ConjureTypeConversion
from subprocess import Popen, PIPE

class ConjureHelper:
    def __init__(self):
        self.tempdir = "./conjure-temp-files"
        if(not os.path.isdir(self.tempdir)):
            os.mkdir(self.tempdir)
    
    def create_temp_file(self, contents:str) -> str:
        temp_filename = next(tempfile._get_candidate_names())
        with open(self.tempdir + "/" + temp_filename, "w") as file:
            file.write(contents)
            file.close()
        return self.tempdir + "/" + temp_filename

    def get_required_params(self, code):
        temp_essence_file = self.create_temp_file(code)
        shell_output = Popen(["conjure ide " + temp_essence_file + " --dump-declarations", ], shell=True, stdout=PIPE, stderr=PIPE)
        output, error = shell_output.communicate()
        if(error):
            raise Exception(error.decode('utf-8'))
        finds = []
        for dec in json.loads(output):
            if dec.get('kind', '') == 'Given':
                finds.append(dec.get('name'))
        return finds

    def create_params_file(self, params = {}):
        if(len(params.keys()) == 0):
            raise Exception("No params are given.")   
        tempstr = "language Essence 1.3\n"
        for key, value in params.items():
            tempstr+=ConjureTypeConversion.toConjureParamText(key, value) # python variable to conjure param text
        return self.create_temp_file(tempstr)

    def read_solution_json_file(self) -> dict:
        solution_nums = 0
        solutions = []
        try:
            if(os.path.isdir('./conjure-output')):
                files = os.listdir('./conjure-output')
                for f in files:
                    if f.endswith('.json'):
                        with open('./conjure-output/' + f) as file:
                            solutions.append(json.loads(file.read()))
                            solution_nums+=1
        except:
            raise Exception('Error while reading json solution file(s).')
        if(solution_nums == 0):
            raise Exception('No solution found for this model.')
        elif(solution_nums == 1):
            return solutions[0]
        else:
            return {"conjure_solutions": solutions}

    def clean_tmp_files(self):
        # remove conjure-output-folder
        if(os.path.isdir('./conjure-output')):
            files = os.listdir('./conjure-output')
            for f in files:
                try:
                    os.remove('./conjure-output/' + f)
                except:
                    pass
        if(os.path.isdir('./conjure-temp-files')):
            files = os.listdir('./conjure-temp-files')
            for f in files:
                try:
                    os.remove('./conjure-temp-files/' + f)
                except:
                    pass
        