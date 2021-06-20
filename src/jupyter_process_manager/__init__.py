"""Entry point for jupyter_process_manager package"""
# Standard library imports

# Third party imports

# Local imports
from jupyter_process_manager.class_processes_manager import \
    JupyterProcessesManager
from . import logger

__all__ = ["JupyterProcessesManager"]

# Create LOGGER for current project
logger.initialize_project_logger(
    name=__name__,
    path_dir_where_to_store_logs="",
    is_stdout_debug=False,
    is_to_propagate_to_root_logger=False,
)
