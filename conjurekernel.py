from ipykernel.kernelbase import Kernel
from conjure import Conjure
class ConjureKernel(Kernel):
    implementation = 'Conjure'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Conjure',
        'mimetype': 'text/plain',
        'file_extension': '.essence',
    }
    banner = "Conjure jupyter notebook"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
               conjure = Conjure()
               try:
                   result = conjure.execute(code)
                   if not silent:
                       stream_content = {'name': 'stdout', 'text': result}
                       self.send_response(self.iopub_socket, 'stream', stream_content)
                       return { 'status': 'ok', 'execution_count': self.execution_count, }
               except Exception as e:
                   if not silent:
                       stream_content = {'name': 'stderr', 'text': e.__str__()}
                       self.send_response(self.iopub_socket, 'stream', stream_content)
                       return { 'status': 'error' }
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ConjureKernel)