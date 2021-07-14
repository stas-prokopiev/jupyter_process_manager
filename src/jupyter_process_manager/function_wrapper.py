"""Decorators and wrappers to redirect streams for processes"""
from __future__ import print_function
# Standard library imports
import sys
import atexit
# from contextlib import redirect_stdout, redirect_stderr

# Third party imports
from char import char

# Local imports

DICT_STREAMS_STATE = {}

def return_stdout_stderr_to_usual_state():
    """Return stdout and stderr back to the previous state"""
    if sys.stdout != DICT_STREAMS_STATE["stdout"]:
        sys.stdout.close()
        sys.stdout = DICT_STREAMS_STATE["stdout"]
    if sys.stderr != DICT_STREAMS_STATE["stderr"]:
        sys.stderr.close()
        sys.stderr = DICT_STREAMS_STATE["stderr"]


@char
def redirect_stdout_stderr_to_files(
        str_stdout_file,
        str_stderr_file,
):
    """Return stdout and stderr to the files"""
    DICT_STREAMS_STATE["stdout"] = sys.stdout
    sys.stdout = open(str_stdout_file, "w", buffering=1)
    DICT_STREAMS_STATE["stderr"] = sys.stderr
    sys.stderr = open(str_stderr_file, 'w', buffering=1)
    atexit.register(return_stdout_stderr_to_usual_state)


@char
def wrapped_func(
        str_stdout_file,
        str_stderr_file,
        func_to_process,
        *args,
        **kwargs
):
    """Wrapper to run function with outputs redirected to files"""
    redirect_stdout_stderr_to_files(
        str_stdout_file,
        str_stderr_file,
    )
    func_to_process(*args, **kwargs)
    return_stdout_stderr_to_usual_state()
