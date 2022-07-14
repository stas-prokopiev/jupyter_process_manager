"""Decorators and wrappers to redirect streams for processes"""
from __future__ import print_function
# Standard library imports
from typing import Optional, Any, Union, Callable, IO
import os
import logging
import sys
import atexit
import threading
from functools import partial
from io import StringIO
import time
import _thread

# Third party imports
from char import char
from IPython.display import clear_output as clear_output_jupyter

# Local imports

DICT_STREAMS_PREV_STATE = {}



@char
def redirect_stdout_stderr(stdout_stream, stderr_stream,) -> None:
    """Return stdout and stderr to the files"""
    DICT_STREAMS_PREV_STATE["stdout"] = sys.stdout
    sys.stdout = stdout_stream
    # sys.stdout = open(str_stdout_file, "r+", buffering=1)
    DICT_STREAMS_PREV_STATE["stderr"] = sys.stderr
    sys.stderr = stderr_stream
    # sys.stderr = open(str_stderr_file, 'r+', buffering=1)
    redirect_all_stream_loggers(sys.stdout, sys.stderr)
    atexit.register(return_stdout_stderr_to_usual_state)




def check_if_output_redirected() -> bool:
    """"""
    if "stdout" not in DICT_STREAMS_PREV_STATE:
        return False
    if sys.stdout == DICT_STREAMS_PREV_STATE["stdout"]:
        return False
    return True



def redirect_outputs_for_main():
    """"""
    stdout_stream = StringIO()
    stderr_stream = StringIO()
    redirect_stdout_stderr(stdout_stream, stderr_stream)







def clear_output() -> None:
    """"""
    clear_output_jupyter()
    try:
        sys.stdout.seek(0)
        sys.stdout.truncate(0)
    except Exception as ex:
        print(f"Unable to clear stdout output: {ex}")
    # clear_output_jupyter()


    # clear_output_jupyter()
    # if "stdout" in DICT_STREAMS_PREV_STATE:
    #     if sys.stdout != DICT_STREAMS_PREV_STATE["stdout"]:
    #         sys.stdout.seek(0)
    #         sys.stdout.truncate(0)


def read_stdout() -> str:
    """"""

    try:
        sys.stdout.seek(0)
        content = sys.stdout.read()
        return content
    except Exception as ex:
        return f"Unable to read stdout content: {ex}"


    # if "stdout" in DICT_STREAMS_PREV_STATE:
    #     if sys.stdout != DICT_STREAMS_PREV_STATE["stdout"]:
    #         sys.stdout.seek(0)  # jump to the start

    # # print(dir(sys.stdout))
    # # return str(sys.stdout)
    # return sys.stdout.read()


def return_stdout_stderr_to_usual_state() -> None:
    """Return stdout and stderr back to the previous state"""
    if sys.stdout != DICT_STREAMS_PREV_STATE["stdout"]:
        sys.stdout.close()
        sys.stdout = DICT_STREAMS_PREV_STATE["stdout"]
    if sys.stderr != DICT_STREAMS_PREV_STATE["stderr"]:
        sys.stderr.close()
        sys.stderr = DICT_STREAMS_PREV_STATE["stderr"]


def redirect_all_stream_loggers(
        stdout_stream : IO[str],
        stderr_stream : IO[str]
) -> None:
    """"""
    dict_all_loggers = logging.Logger.manager.loggerDict
    for str_full_logger_name in dict_all_loggers:
        logger_tmp = dict_all_loggers[str_full_logger_name]
        if not hasattr(logger_tmp, "handlers"):
            continue
        for handler_obj in logger_tmp.handlers:
            if isinstance(handler_obj, logging.StreamHandler):
                if not hasattr(handler_obj, "stream"):
                    continue
                if not hasattr(handler_obj.stream, "name"):
                    continue
                if handler_obj.stream.name == "<stdout>":
                    handler_obj.setStream(stdout_stream)
                if handler_obj.stream.name == "<stderr>":
                    handler_obj.stream = stderr_stream



def listen_to_jpm_error_file(str_jpm_stderr_file : str) -> None:
    """"""
    if os.path.exists(str_jpm_stderr_file):
        try:
            os.remove(str_jpm_stderr_file)
        except Exception:
            pass
    while True:
        time.sleep(1)
        if os.path.exists(str_jpm_stderr_file):
            _thread.interrupt_main()


@char
def wrapped_func(
        str_stdout_file : str,
        str_stderr_file : str,
        str_jpm_stderr_file : str,
        func_to_process : Callable,
        *args : Any,
        **kwargs : Any
) -> None:
    """Wrapper to run function with outputs redirected to files"""
    stdout_stream = open(str_stdout_file, "r+", buffering=1)
    stderr_stream = open(str_stderr_file, 'r+', buffering=1)
    redirect_stdout_stderr(stdout_stream, stderr_stream,)
    threading.Thread(
        target=partial(listen_to_jpm_error_file, str_jpm_stderr_file),
        daemon=True,
    ).start()
    print("Test that jupyter_process_manager redirected stdout to file")
    func_to_process(*args, **kwargs)
    return_stdout_stderr_to_usual_state()
