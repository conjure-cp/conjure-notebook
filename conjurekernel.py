from ipykernel.kernelbase import Kernel
import tempfile
import os
import base64
from subprocess import Popen, PIPE

class ConjureKernel(Kernel):
    implementation = 'Conjure'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Conjure jupyter notebook"

    async def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        temp_filename = next(tempfile._get_candidate_names())
        temp_essence_file = temp_filename + '.essence'
        with open(temp_essence_file, 'w') as f:
            f.write(str(code))
        shell_output = Popen(["conjure solve -ac " +temp_essence_file + " --output-format=json", ], shell=True, stdout=PIPE, stderr=PIPE)
        _, error = shell_output.communicate()
        if error:
            if not silent:
                stream_content = {'name': 'stdout', 'text': error.decode("utf-8")}
                self.send_response(self.iopub_socket, 'stream', stream_content)
                return {
                'status': 'error',
               }
        else:
            with open('./conjure-output/model000001-solution000001.solution.json') as f:
                contents = f.read()
                if not silent:
                    stream_content = {'name': 'stdout', 'text': contents}
                    self.send_response(self.iopub_socket, 'stream', stream_content)
                os.remove(temp_essence_file)
                os.remove(temp_filename + '.solution')
            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ConjureKernel)