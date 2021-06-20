# -*- coding: utf-8 -*-
from jupyter_process_manager import JupyterProcessesManager
from jupyter_process_manager.test_functions import test_func


def test_basic_functionality_of_jupyter_process_manager():
    """"""
    process_manager = JupyterProcessesManager(".")
    for wait_for_me in range(1, 5):
        process_manager.add_function_to_processing(test_func, wait_for_me)
    process_manager.wait_till_all_processes_are_over(int_seconds_step=2)
