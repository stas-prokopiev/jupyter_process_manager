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
import time
import _thread

# Third party imports
from char import char
from IPython.display import clear_output as clear_output_jupyter

# Local imports

DICT_STREAMS_PREV_STATE = {}


def clear_output() -> None:
    """"""
    clear_output_jupyter()
    if "stdout" in DICT_STREAMS_PREV_STATE:
        if sys.stdout != DICT_STREAMS_PREV_STATE["stdout"]:
            sys.stdout.truncate(0)


def read_stdout() -> str:
    """"""
    sys.stdout.seek(0)  # jump to the start
    return sys.stdout.read()


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


@char
def redirect_stdout_stderr_to_files(
        str_stdout_file : str,
        str_stderr_file : str,
) -> None:
    """Return stdout and stderr to the files"""
    DICT_STREAMS_PREV_STATE["stdout"] = sys.stdout
    sys.stdout = open(str_stdout_file, "w", buffering=1)
    DICT_STREAMS_PREV_STATE["stderr"] = sys.stderr
    sys.stderr = open(str_stderr_file, 'w', buffering=1)
    redirect_all_stream_loggers(sys.stdout, sys.stderr)
    atexit.register(return_stdout_stderr_to_usual_state)


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
        # if not os.path.exists(str_jpm_stderr_file):
        #     continue
        # with open(str_jpm_stderr_file, "r") as f:
        #     content = f.read()
        #     if content:
        #         _thread.interrupt_main()


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
    redirect_stdout_stderr_to_files(
        str_stdout_file,
        str_stderr_file,
    )
    threading.Thread(
        target=partial(listen_to_jpm_error_file, str_jpm_stderr_file),
        daemon=True,
    ).start()
    print("Test that jupyter_process_manager redirected stdout to file")
    func_to_process(*args, **kwargs)
    return_stdout_stderr_to_usual_state()
