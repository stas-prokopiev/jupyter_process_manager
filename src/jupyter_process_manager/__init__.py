"""Entry point for jupyter_process_manager package"""
# Standard library imports

# Third party imports

# Local imports
from jupyter_process_manager.class_processes_manager import \
    JupyterProcessesManager
from . import logger
from .function_wrapper import clear_output
from .function_wrapper import read_stdout
from .function_wrapper import check_if_output_redirected
from .function_wrapper import redirect_outputs_for_main


JupyterProcessManager = JupyterProcessesManager
JPM = JupyterProcessesManager


__all__ = [
    "JupyterProcessesManager", "JupyterProcessManager", "JPM",
    "clear_output", "read_stdout",
    "check_if_output_redirected", "redirect_outputs_for_main",
]

# Create LOGGER for current project
logger.initialize_project_logger(
    name=__name__,
    path_dir_where_to_store_logs="",
    is_stdout_debug=False,
    is_to_propagate_to_root_logger=False,
)
