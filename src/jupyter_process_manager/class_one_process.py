"""Module with class for all operations with one process"""
from __future__ import print_function
# Standard library imports
import os
import logging
from multiprocessing import Process
import datetime

# Third party imports
from local_simple_database import LocalSimpleDatabase

# Local imports
from .function_wrapper import wrapped_func
from .other import timedelta_nice_format

LOGGER = logging.getLogger(__name__)


class OneProcess(object):
    """Class with object to handle all operations related to 1 process
    """

    def __init__(self, str_dir_for_output):
        """"""
        self.str_dir_for_output = str_dir_for_output
        self.int_process_id = self._get_id_for_new_process()
        self.str_stdout_file, self.str_stderr_file = \
            self._create_files_for_stdout_and_stderr()
        self.process = None
        self.dt_start_time = None
        self.dt_finish_time = None
        self.is_error_happened = None
        self.str_status = "Not Started"

    def __del__(self):
        """Terminate current process"""
        self.terminate()

    def start_process(self, func_to_process, *args, **kwargs):
        """Run given function as separate process with given arguments

        Args:
            func_to_process (function): Function which to run
            *args: All arguments
            **kwargs: All arguments

        """
        new_args = (
            self.str_stdout_file, self.str_stderr_file, func_to_process) + args
        new_process = Process(target=wrapped_func, args=new_args, kwargs=kwargs)
        new_process.daemon = True
        new_process.start()
        self.process = new_process
        self.dt_start_time = datetime.datetime.now()

    def debug_run_of_the_func(self, func_to_process, *args, **kwargs):
        """
        Run given function in the current process to check that it is runnable
        """
        new_args = (
            self.str_stdout_file, self.str_stderr_file, func_to_process, args)
        wrapped_func(*new_args, **kwargs)

    def is_alive(self):
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

    def get_how_long_this_process_is_running(self):
        """Get string with duration this process is running"""
        if not self.dt_start_time:
            return "None"
        if self.dt_finish_time:
            return timedelta_nice_format(self.dt_finish_time - self.dt_start_time)
        return timedelta_nice_format(datetime.datetime.now() - self.dt_start_time)

    def get_full_process_output(self):
        """Get string with full STDOUT output of the process"""
        if not self.str_stdout_file:
            return ""
        with open(self.str_stdout_file, "r") as file_handler:
            str_whole_stdout_file = file_handler.read()
        return str_whole_stdout_file

    def get_last_n_lines_of_stdout(self, int_last_lines=100):
        """Get last N line of STDOUT output of the process"""
        str_whole_output = self.get_full_process_output()
        list_lines = str_whole_output.splitlines()
        if not list_lines:
            return "STDOUT OUTPUT IS EMPTY"
        if len(list_lines) < int_last_lines:
            return str_whole_output
        return "\n".join(list_lines[-int_last_lines:])

    def terminate(self):
        """Terminate current process"""
        if self.process.is_alive():
            LOGGER.debug(
                "Closing procees %d", self.int_process_id, flush=True)
            self.process.terminate()
            self.str_status = "Terminated by user"
            self.dt_finish_time = datetime.datetime.now()

    def get_full_process_errors(self):
        """Get string with full STDERR output of the process"""
        if not self.str_stderr_file:
            return ""
        with open(self.str_stderr_file, "r") as file_handler:
            str_whole_stderr_file = file_handler.read()
        if not str_whole_stderr_file:
            return "STDERR OUTPUT IS EMPTY"
        return str_whole_stderr_file

    def get_last_error_msg(self):
        """Get string with last ERROR message"""
        list_errors = self.get_list_all_errors()
        if not list_errors:
            return ""
        return list_errors[-1]

    def get_list_all_errors(self):
        """Get list with all ERRORs from STDERR"""
        str_whole_error_file = self.get_full_process_errors()
        list_errors = str_whole_error_file.split("Traceback ")
        if len(list_errors) <= 1:
            return []
        list_errors_full = [
            "Traceback " + str_error
            for str_error in list_errors[1:]
            if str_error]
        return list_errors_full

    def _is_error_happened(self):
        """Check if any ERROR happened with current process"""
        if self.get_last_error_msg():
            return True
        return False

    def _get_id_for_new_process(self):
        """Get unique ID for the current process"""
        self.LSD = LocalSimpleDatabase(self.str_dir_for_output)
        self.LSD["int_max_used_process_id"] += 1
        return self.LSD["int_max_used_process_id"]

    def _create_files_for_stdout_and_stderr(self):
        """Create files where to redirect STDOUT and STDERR"""
        str_stdout_file = os.path.join(
            self.str_dir_for_output, "stdout_%d.txt" % self.int_process_id)
        str_stderr_file = os.path.join(
            self.str_dir_for_output, "stderr_%d.txt" % self.int_process_id)
        return str_stdout_file, str_stderr_file
