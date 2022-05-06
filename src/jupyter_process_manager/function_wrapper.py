"""Decorators and wrappers to redirect streams for processes"""
from __future__ import print_function
# Standard library imports
import logging
import sys
import atexit

# Third party imports
from char import char
from IPython.display import clear_output as clear_output_jupyter

# Local imports

DICT_STREAMS_STATE = {}




def clear_output():
    """"""
    clear_output_jupyter()
    if "stdout" in DICT_STREAMS_STATE:
        if sys.stdout != DICT_STREAMS_STATE["stdout"]:
            sys.stdout.truncate(0)


def return_stdout_stderr_to_usual_state():
    """Return stdout and stderr back to the previous state"""
    if sys.stdout != DICT_STREAMS_STATE["stdout"]:
        sys.stdout.close()
        sys.stdout = DICT_STREAMS_STATE["stdout"]
    if sys.stderr != DICT_STREAMS_STATE["stderr"]:
        sys.stderr.close()
        sys.stderr = DICT_STREAMS_STATE["stderr"]


def redirect_all_stream_loggers(stdout_stream, stderr_stream):
    """"""
    dict_all_loggers = logging.Logger.manager.loggerDict
    for str_full_logger_name in dict_all_loggers:
        logger_tmp = dict_all_loggers[str_full_logger_name]
        if not hasattr(logger_tmp, "handlers"):
            continue
        # print(str_full_logger_name)
        for handler_obj in logger_tmp.handlers:
            if isinstance(handler_obj, logging.StreamHandler):
                # print(dir(handler_obj))
                # handler_obj.emit
                # handler_obj.setStream
                # handler_obj.stream
                # print("---> Stream: ", handler_obj.stream)
                # print("------> Name: ", handler_obj.stream.name)
                # print("------> ", handler_obj.stream.name == "<stdout>")
                # if handler_obj.stream == DICT_STREAMS_STATE["stdout"]:
                if not hasattr(handler_obj, "stream"):
                    continue
                if not hasattr(handler_obj.stream, "name"):
                    continue
                if handler_obj.stream.name == "<stdout>":
                    handler_obj.setStream(stdout_stream)
                # if handler_obj.stream == DICT_STREAMS_STATE["stderr"]:
                if handler_obj.stream.name == "<stderr>":
                    handler_obj.stream = stderr_stream


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
    redirect_all_stream_loggers(sys.stdout, sys.stderr)
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
    print("Test that jupyter_process_manager redirected stdout to file")
    func_to_process(*args, **kwargs)
    return_stdout_stderr_to_usual_state()
