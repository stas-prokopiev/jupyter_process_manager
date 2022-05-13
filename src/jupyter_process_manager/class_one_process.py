"""Module with class for all operations with one process"""
from __future__ import print_function
# Standard library imports
from typing import Optional, Any, Union, Callable
import sys
import os
import logging
from multiprocessing import Process
import datetime
import time

# Third party imports
from local_simple_database import LocalSimpleDatabase
import psutil
from round_to_n_significant_digits import rtnsd
from timedelta_nice_format import timedelta_nice_format

# Local imports
from .function_wrapper import wrapped_func


LOGGER = logging.getLogger(__name__)


class OneProcess(object):
    """Class with object to handle all operations related to 1 process
    """

    def __init__(
            self,
            str_dir_for_output : str,
            str_proc_name : str = ""
    ) -> None:
        """"""
        self.str_dir_for_output = str_dir_for_output
        self.int_process_id = self._get_id_for_new_process()
        self.str_stdout_file = os.path.join(
            self.str_dir_for_output, "stdout_%d.txt" % self.int_process_id)
        self.str_stderr_file = os.path.join(
            self.str_dir_for_output, "stderr_%d.txt" % self.int_process_id)
        self.str_jpm_stderr_file = os.path.join(
            self.str_dir_for_output, "jpm_stderr_%d.txt" % self.int_process_id)

        with open(self.str_stdout_file, "w"): pass
        with open(self.str_stderr_file, "w"): pass


        self.process = None
        self.dt_start_time = None
        self.dt_finish_time = None
        self.is_error_happened = None
        self.str_status = "Not Started"
        self.str_proc_name = str_proc_name

    def __del__(self) -> None:
        """Terminate current process"""
        self.terminate()

    def start_process(
            self,
            func_to_process : Callable,
            *args : Any,
            **kwargs : Any
    ) -> None:
        """Run given function as separate process with given arguments

        Args:
            func_to_process (function): Function which to run
            *args: All arguments
            **kwargs: All arguments

        """
        new_args = (
            self.str_stdout_file,
            self.str_stderr_file,
            self.str_jpm_stderr_file,
            func_to_process
        ) + args
        new_process = Process(target=wrapped_func, args=new_args, kwargs=kwargs)
        new_process.daemon = True
        new_process.start()
        self.process = new_process
        self.dt_start_time = datetime.datetime.now()

    def debug_run_of_the_func(
            self,
            func_to_process : Callable,
            *args : Any,
            **kwargs : Any
    ) -> None:
        """
        Run given function in the current process to check that it is runnable
        """
        new_args = (
            self.str_stdout_file, self.str_stderr_file, func_to_process, args)
        wrapped_func(*new_args, **kwargs)

    def is_alive(self) -> bool:
        """Check if process is alive and save current state of the process"""
        if self.process is None:
            self.str_status = "Not Started"
            return False
        if self.is_error_happened:
            self.str_status = "Error"
            return False
        if self.str_status == "Terminated by user":
            return False
        if self.dt_finish_time:
            self.str_status = "Finished"
            return False
        if not self.process.is_alive():
            self.dt_finish_time = datetime.datetime.now()
            self.is_error_happened = self._is_error_happened()
            if self.is_error_happened:
                self.str_status = "Error"
            else:
                self.str_status = "Just Finished"
            return False
        self.str_status = "Running"
        return True

    def get_pid(self) -> Optional[int]:
        """Get current process ID"""
        if self.is_alive():
            return self.process.pid
        return None

    def get_mem_usage(self) -> str:
        """Get current process RAM memory usage string in nice format"""
        if self.dt_finish_time:
            return "None"
        process = psutil.Process(self.get_pid())
        if not process:
            return "None"
        int_mem_bytes = process.memory_info().rss
        float_mem_mbytes = int_mem_bytes / 1024.0 / 1024.0
        if float_mem_mbytes > 1024:
            float_mem_gbytes = float_mem_mbytes / 1024.0
            return str(rtnsd(float_mem_gbytes, 2)) + " Gb"
        return str(rtnsd(float_mem_mbytes, 2)) + " Mb"

    def get_how_long_this_process_is_running(self) -> str:
        """Get string with duration this process is running"""
        if not self.dt_start_time:
            return "None"
        if self.dt_finish_time:
            return timedelta_nice_format(self.dt_finish_time - self.dt_start_time)
        return timedelta_nice_format(datetime.datetime.now() - self.dt_start_time)

    def get_stdout(self) -> str:
        """Get last N line of STDOUT output of the process"""
        if not self.str_stdout_file:
            return "ERROR: Path to file with stdout is not given"
        if not os.path.exists(self.str_stdout_file):
            with open(self.str_stdout_file, "w"): pass
            return "STDOUT OUTPUT IS EMPTY"
        with open(self.str_stdout_file, "r") as file_handler:
            str_whole_output = file_handler.read()
        list_lines = str_whole_output.splitlines()
        if not list_lines:
            return "STDOUT OUTPUT IS EMPTY"
        return str_whole_output

    def terminate(self) -> None:
        """Terminate current process"""
        if self.process.is_alive():
            LOGGER.info("Closing procees %d", self.int_process_id)
            LOGGER.info(
                "---> Try to close the process by raising KeyboardInterupt")
            with open(self.str_jpm_stderr_file, "w") as f:
                f.write("Stop process by JupyterProcessManager")
            for _ in range(50):
                time.sleep(0.1)
                if not self.process.is_alive():
                    LOGGER.info("------> Process was stopped.")
                    break
            else:
                LOGGER.info(
                    "------> Process HASN'T stopped by KeyboardInterupt.")
                LOGGER.info(
                    "---> Terminate the process by telling OS to kill it")
                self.process.terminate()
            self.str_status = "Terminated by user"
            self.dt_finish_time = datetime.datetime.now()

    def get_list_all_errors(self) -> list[str]:
        """Get list with all ERRORs from STDERR"""
        if not self.str_stderr_file:
            return ""
        with open(self.str_stderr_file, "r") as file_handler:
            str_whole_stderr_file = file_handler.read()
        if not str_whole_stderr_file:
            return "STDERR OUTPUT IS EMPTY"
        list_errors = str_whole_stderr_file.split("Traceback ")
        if len(list_errors) <= 1:
            return []
        list_errors_full = [
            "Traceback " + str_error
            for str_error in list_errors[1:]
            if str_error]
        return list_errors_full

    def get_last_error_msg(self) -> str:
        """Get string with last ERROR message"""
        list_errors = self.get_list_all_errors()
        if not list_errors:
            return ""
        return list_errors[-1]

    def _is_error_happened(self) -> bool:
        """Check if any ERROR happened with current process"""
        if self.get_last_error_msg():
            return True
        return False

    def _get_id_for_new_process(self) -> int:
        """Get unique ID for the current process"""
        self.LSD = LocalSimpleDatabase(self.str_dir_for_output)
        self.LSD["int_max_used_process_id"] += 1
        return self.LSD["int_max_used_process_id"]
