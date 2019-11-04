import sys
from io import StringIO
import threading
import time
from code import InteractiveInterpreter


def execute(interpreter: InteractiveInterpreter, code):
    old_stdout, old_stderr = sys.stdout, sys.stderr
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    interpreter.runcode(code)
    sys.stdout, sys.stderr = old_stdout, old_stdout
    return {'output': redirected_output.getvalue(), 'error': redirected_error.getvalue()}


clients = {}


class Client(threading.Thread):
    def __init__(self, queue: list, id):
        super().__init__()
        self.id = id
        self.queue = queue
        self.result = []
        variables = globals().copy()
        variables.update(locals())
        self.interpreter = InteractiveInterpreter(variables)
        self.stop = False
        self.loading = False

    def run(self):
        self.interpreter.runcode("__name__ = '__main__'")
        while True:
            while len(self.queue) > 0:
                self.loading = True
                code = self.queue.pop(0)
                self.result.append(execute(self.interpreter, code))
                self.loading = False
            time.sleep(1)
            if self.stop:
                break

    def push_code(self, code):
        self.queue.append(code)

    def get_result(self):
        while len(self.result) <= 0:
            pass
        result = self.result.pop(0)
        return result

    def close_client(self):
        self.stop = True


class IDError(Exception):
    def __init__(self, error):
        super().__init__(self)
        self.error = error
        pass

    def __repr__(self):
        return self.error

    def __str__(self):
        return self.error
