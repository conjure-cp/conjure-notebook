from ipykernel.kernelbase import Kernel
import os

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

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        with open('first.essence', 'w') as f:
            f.write(str(code))
        os.system('conjure solve -ac first.essence --output-format=json')
        with open('./conjure-output/model000001-solution000001.solution.json') as f:
            contents = f.read()
            if not silent:
                stream_content = {'name': 'stdout', 'text': contents}
                self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ConjureKernel)