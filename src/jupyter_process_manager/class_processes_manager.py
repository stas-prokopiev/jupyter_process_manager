"""Main module with class which helps in handing many processes"""
from __future__ import print_function
from __future__ import unicode_literals
# Standard library imports
import os
import logging
from collections import OrderedDict
from time import sleep
import datetime

# Third party imports
from IPython.display import clear_output
from IPython.display import display
from IPython import get_ipython
from IPython.display import HTML
from tabulate import tabulate
from yaspin import yaspin
from char import char

# Local imports
from .class_one_process import OneProcess
from .other import timedelta_nice_format
from . import widget

LOGGER = logging.getLogger(__name__)


class JupyterProcessesManager(object):
    """Class to handle creation and showing output for many processes"""

    @char
    def __init__(
            self,
            str_dir_for_output,
            is_to_delete_previous_outputs=True
    ):
        """Initialize object

        Args:
            str_dir_for_output (str): Path to dir where to store output files
            is_to_delete_previous_outputs (bool, optional): \
                Flag if to delete previous output files
        """
        self.int_processes = 0
        # Create directory where to store processes output
        str_processes_output_dir = os.path.join(
            str_dir_for_output, "processes_output")
        if not os.path.exists(str_processes_output_dir):
            os.makedirs(str_processes_output_dir)
        self.str_dir_for_output = str_processes_output_dir
        if is_to_delete_previous_outputs:
            self._delete_all_previous_outputs()
        self.dict_all_processes_by_id = OrderedDict()
        self.dict_alive_processes_by_id = OrderedDict()
        self.dt_processes_started_at = None

    @char
    def add_function_to_processing(self, func_to_process, *args, **kwargs):
        """Start running function as process

        Args:
            func_to_process (function): Function to add for processing
        """
        new_process = OneProcess(self.str_dir_for_output)
        new_process.start_process(func_to_process, *args, **kwargs)
        if not self.dict_alive_processes_by_id:
            self.dt_processes_started_at = datetime.datetime.now()
        self.dict_all_processes_by_id[new_process.int_process_id] = new_process
        self.dict_alive_processes_by_id[new_process.int_process_id] = new_process

    @char
    def debug_run_of_1_function(self, func_to_process, *args, **kwargs):
        """
        Run given function in the current process to check that it is runnable
        """
        new_process = OneProcess(self.str_dir_for_output)
        new_process.debug_run_of_the_func(func_to_process, *args, **kwargs)
        self.dict_all_processes_by_id[new_process.int_process_id] = new_process
        self.dict_alive_processes_by_id[new_process.int_process_id] = new_process

    @char
    def wait_till_all_processes_are_over(
            self,
            int_seconds_step=10,
            int_max_processes_to_show=20
    ):
        """Wait while processes are running and print information during it

        Args:
            int_seconds_step (int,): Seconds to update processes info
            int_max_processes_to_show (int): \
                Max number of processes to show at once in the table
        """
        clear_output(wait=True)
        self.print_info_about_running_processes(
            int_max_processes_to_show=int_max_processes_to_show)
        try:
            while True:
                if not self.dict_alive_processes_by_id:
                    break
                with yaspin() as spinner_obj:
                    for i in range(int_seconds_step):
                        spinner_obj.text = "Updating in {} seconds".format(
                            int_seconds_step - i)
                        sleep(1)
                clear_output(wait=True)
                self.print_info_about_running_processes(
                    int_max_processes_to_show=int_max_processes_to_show)
        except KeyboardInterrupt:
            clear_output(wait=True)
            print("Interrupting running processes")
            self.terminate_all_alive_processes()
            print("---> Done")
        print("All processes were finished")

    @char
    def terminate_all_alive_processes(self):
        """Terminate all alive processes"""
        print("Terminating all alive processes")
        for process_num in list(self.dict_alive_processes_by_id):
            print("---> Terminate process: ", process_num + 1)
            process_obj = self.dict_alive_processes_by_id[process_num]
            process_obj.terminate()
            if not process_obj.is_alive():
                self.dict_alive_processes_by_id.pop(process_num, None)
                print("------> Done")

    @char
    def show_jupyter_widget(
            self,
            int_seconds_step=10,
            int_max_processes_to_show=20
    ):
        """Show jupyter widget to interact with running processes

        Args:
            int_seconds_step (int,): Seconds to update processes info
            int_max_processes_to_show (int): \
                Max number of processes to show at once in the table
        """
        clear_output(wait=True)
        app_gui = widget.create_jupyter_widget(self)
        display(app_gui)
        with widget.OUTPUT_PROCESSES_CONDITIONS:
            self.print_info_about_running_processes(
                int_max_processes_to_show=int_max_processes_to_show)
        try:
            while True:
                if not self.dict_alive_processes_by_id:
                    break
                for _ in range(int_seconds_step):
                    sleep(0.2)
                    get_ipython().kernel.do_one_iteration()
                widget.OUTPUT_PROCESSES_CONDITIONS.clear_output(wait=True)
                with widget.OUTPUT_PROCESSES_CONDITIONS:
                    self.print_info_about_running_processes(
                        int_max_processes_to_show=int_max_processes_to_show)
        except KeyboardInterrupt:
            clear_output(wait=True)
            print("Interrupting running processes")
            self.terminate_all_alive_processes()
            print("---> Done")
        print("All processes were finished")

    @char
    def print_info_about_running_processes(self, int_max_processes_to_show=20):
        """Print information string about current processes"""
        display(HTML("<h2>Processes conditions:</h2>"))
        # print("Conditions of the processes:")
        if self.dt_processes_started_at:
            timedelta = datetime.datetime.now() - self.dt_processes_started_at
            print("Working for:", timedelta_nice_format(timedelta))
        self.print_table_with_conditions(
            int_max_processes_to_show=int_max_processes_to_show)
        print(
            "ALIVE PROCESSES: ",
            len(self.dict_alive_processes_by_id), "/",
            len(self.dict_all_processes_by_id))

    @char
    def print_table_with_conditions(self, int_max_processes_to_show=20):
        """Print table with processes conditions"""
        list_list_processes_info = []
        list_headers = ["Process Id", "Status", "Runtime"]
        for process_num in list(self.dict_all_processes_by_id):
            list_process_info = []
            process_obj = self.dict_all_processes_by_id[process_num]
            # Delete if process is not alive
            if process_num in list(self.dict_alive_processes_by_id):
                if not process_obj.is_alive():
                    self.dict_alive_processes_by_id.pop(process_num, None)
            # "Process Id"
            list_process_info.append(process_num)
            # "Status"
            list_process_info.append(process_obj.str_status)
            # "Runtime"
            str_runtime = process_obj.get_how_long_this_process_is_running()
            list_process_info.append(str_runtime)
            list_list_processes_info.append(list_process_info)
        if len(list_list_processes_info) > int_max_processes_to_show:
            list_list_additional_columns = []
            list_list_additional_columns.append(["---", "---", "---"])
            str_num = str(
                len(list_list_processes_info) - int_max_processes_to_show)
            list_list_additional_columns.append(
                ["Processes", "Hidden", str_num])
            list_list_additional_columns.append(["---", "---", "---"])
            list_list_processes_info = \
                list_list_additional_columns + list_list_processes_info[:20]
        # github  psql  orgtbl  pretty
        print(tabulate(
            list_list_processes_info, headers=list_headers, tablefmt="pretty"))

    def _delete_all_previous_outputs(self):
        """Delete outputs of all previous processes"""
        for str_filename in os.listdir(self.str_dir_for_output):
            str_file_path = os.path.join(self.str_dir_for_output, str_filename)
            if not os.path.isfile(str_file_path):
                continue
            if "stdout_" in str_filename or "stderr_" in str_filename:
                try:
                    os.remove(str_file_path)
                except Exception as ex:
                    print("Cant DELETE previous thread file: ", str_filename)
                    print(ex)
