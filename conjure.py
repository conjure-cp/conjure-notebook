import sys
import os
import tempfile
import json
from subprocess import Popen, PIPE

class Conjure:
    def solve(self, code, params = None):
        temp_filename = next(tempfile._get_candidate_names())
        temp_essence_file = temp_filename + '.essence'
        temp_params_file = temp_filename + '.essence-param'
        with open(temp_essence_file, 'w') as f:
            f.write(str(code))
            f.close()

        if params:
            self.create_params_file(temp_params_file, params)
            shell_output = Popen(["conjure solve -ac " + temp_essence_file + " " + temp_params_file +" --output-format=json", ], shell=True, stdout=PIPE, stderr=PIPE)
        else:
            shell_output = Popen(["conjure solve -ac " + temp_essence_file + " --output-format=json", ], shell=True, stdout=PIPE, stderr=PIPE)

        _, error = shell_output.communicate()
        if(error):
            self.clean_tmp_files()
            raise Exception(error.decode('utf-8'))
        try:
            with open(self.get_solution_json_file()) as f:
                self.clean_tmp_files()
                return f.read()
        except Exception as e:
            print(e, file = sys.stderr) # print error to strerr
            self.clean_tmp_files()
            raise Exception("Interenal error occured")
    
    def get_required_params(self, code):
        temp_filename = next(tempfile._get_candidate_names())
        temp_essence_file = temp_filename + '.essence'
        with open(temp_essence_file, 'w') as f:
            f.write(str(code))
            f.close()
        shell_output = Popen(["conjure ide " + temp_essence_file + " --dump-declarations", ], shell=True, stdout=PIPE, stderr=PIPE)
        output, error = shell_output.communicate()
        finds = []
        for dec in json.loads(output):
            if dec.get('kind', '') == 'Given':
                finds.append(dec.get('name'))
        return finds
        
    def get_solution_json_file(self):
        if(os.path.isdir('./conjure-output')):
            files = os.listdir('./conjure-output')
            for f in files:
                if f.endswith('.json'):
                    return './conjure-output/' + f
        raise(Exception('No json solution file found in conjure-output directory.'))

    def create_params_file(self, temp_params_file, params):
        with open(temp_params_file, 'w') as f:
            tempstr = "language Essence 1.3\n"
            for key, value in params.items():
                tempstr+="letting {0} be {1}\n".format(key, value)
            f.write(tempstr)
            f.close()

    def clean_tmp_files(self):
        files = os.listdir('.')
        for f in files:
            if f.endswith('.essence') or f.endswith('.solution') or f.endswith('.essence-param'):
                try:
                    os.remove(f)
                except:
                    pass
         # remove conjure-output-folder
        if(os.path.isdir('./conjure-output')):
            files = os.listdir('./conjure-output')
            for f in files:
                try:
                    os.remove('./conjure-output/' + f)
                except:
                    pass