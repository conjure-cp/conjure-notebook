import sys
import os
import tempfile
from subprocess import Popen, PIPE

class Conjure:
    def execute(self, code):
        temp_filename = next(tempfile._get_candidate_names())
        temp_essence_file = temp_filename + '.essence'
        solution_json_file = './conjure-output/model000001-solution000001.solution.json'
        with open(temp_essence_file, 'w') as f:
            f.write(str(code))
        shell_output = Popen(["conjure solve -ac " + temp_essence_file + " --output-format=json", ], shell=True, stdout=PIPE, stderr=PIPE)
        _, error = shell_output.communicate()
        if(error):
            self.clean_tmp_files()
            raise Exception(error.decode('utf-8'))
        try:
            with open(solution_json_file) as f:
                self.clean_tmp_files()
                return f.read()
        except Exception as e:
            print(e, file = sys.stderr) # print error to strerr
            self.clean_tmp_files()
            raise Exception("Interenal error occured")

    def clean_tmp_files(self):
        files = os.listdir()
        for f in files:
            if f.endswith('.essence') or f.endswith('.solution'):
                try:
                    os.remove(f)
                except:
                    pass