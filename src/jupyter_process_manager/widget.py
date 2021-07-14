"""Module with functions to handle all ipywidget stuff"""
from __future__ import print_function
# Standard library imports

# Third party imports
import ipywidgets
from ipywidgets import HBox
from ipywidgets import VBox

# Local imports

MAIN_VBOX_LAYOUT = dict(
    width="100%",
    justify_content="center",
    align_self="center",
    padding="0px 0px 10px 0px"

)

HBOX_LAYOUT = dict(
    flex_wrap="wrap",
    flex="1 1 auto",
    width="80%",
    justify_content="center",
    align_self="center",
    padding="10px 0px 0px 0px"
)

VBOX_APP_GUI = VBox()
VBOX_MAIN_GUI = VBox(layout=MAIN_VBOX_LAYOUT)
VBOX_CHOOSE_OUTPUT = VBox()
VBOX_CHOOSE_OUTPUT_TYPE = VBox()
VBOX_ONE_PROCESS_CHOOSE_OUTPUT = VBox()

HBOX_BUTTONS_TO_STOP_PROCESSES = HBox()


OUTPUT_PROCESSES_CONDITIONS = ipywidgets.Output()
OUTPUT = ipywidgets.Output()
BUTTONS_CHOOSE_PROCESS = ipywidgets.ToggleButtons()
WIDGET_LAST_LINES_TO_GET = ipywidgets.IntText(100)


def update_one_process_choose_output(process_manager_obj):
    """Create all widgets with buttons to show output

    Args:
        process_manager_obj (JupyterProcessesManager): Processes manager
    """
    list_buttons = []
    #####
    # BUTTON STDOUT
    button_show_stdout = ipywidgets.Button(
        description='Show process STDOUT',
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        layout={"width": "200px"}
    )
    def on_click_stdout(_):
        """"""
        OUTPUT.clear_output(wait=True)
        int_chosen_process = BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        str_output = process_obj.get_last_n_lines_of_stdout(
            int_last_lines=WIDGET_LAST_LINES_TO_GET.value)
        with OUTPUT:
            print(str_output)
    button_show_stdout.on_click(on_click_stdout)
    list_buttons.append(button_show_stdout)
    #####
    # BUTTON STDERR
    button_show_stderr = ipywidgets.Button(
        description='Show LAST ERROR',
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        layout={"width": "200px"}
    )
    def on_click_stderr(_):
        """"""
        OUTPUT.clear_output(wait=True)
        int_chosen_process = BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        int_errors_happened = len(process_obj.get_list_all_errors())
        with OUTPUT:
            print("ERROR found: ", int_errors_happened)
            if int_errors_happened:
                str_last_error = process_obj.get_last_error_msg()
                print("Last error message: ")
                print(str_last_error)
    button_show_stderr.on_click(on_click_stderr)
    list_buttons.append(button_show_stderr)
    #####
    # BUTTON STOP PROCESS
    int_chosen_process = BUTTONS_CHOOSE_PROCESS.value
    process_obj = \
        process_manager_obj.dict_all_processes_by_id[int_chosen_process]
    if process_obj.is_alive():
        button_stop_process = ipywidgets.Button(
            description='STOP %d process' % int_chosen_process,
            button_style='warning',
            layout={"width": "200px"}
        )

        def on_click_stop_process(_):
            """"""
            OUTPUT.clear_output(wait=True)
            int_chosen_process = BUTTONS_CHOOSE_PROCESS.value
            process_obj = \
                process_manager_obj.dict_all_processes_by_id[int_chosen_process]
            with OUTPUT:
                print("Stopping process: ", int_chosen_process)
                process_obj.terminate()
                print("---> Done. Process %d TERMINATED" % int_chosen_process)
        button_stop_process.on_click(on_click_stop_process)
        list_buttons.append(button_stop_process)
    #####
    list_hboxes = []
    list_hboxes.append(
        HBox(
            [ipywidgets.HTML("<h3>Process: %d:</h3>" % int_chosen_process)],
            layout=HBOX_LAYOUT)
    )
    wid_label = ipywidgets.Label("Last STDOUT lines to show:")
    list_hboxes.append(
        HBox([wid_label, WIDGET_LAST_LINES_TO_GET], layout=HBOX_LAYOUT))
    list_hboxes.append(HBox(list_buttons, layout=HBOX_LAYOUT))
    VBOX_ONE_PROCESS_CHOOSE_OUTPUT.children = list_hboxes


def create_choose_process(process_manager_obj):
    """Create all widgets starting from choose process

    Args:
        process_manager_obj (JupyterProcessesManager): Processes manager
    """
    list_hboxes = []
    # Stop ALL Processes
    button_stop_all_processes = ipywidgets.Button(
        description='STOP ALL processes',
        button_style='warning',
        layout={"width": "200px"}
    )
    def on_click_stop_all_processes(_):
        """"""
        OUTPUT.clear_output(wait=True)
        with OUTPUT:
            process_manager_obj.terminate_all_alive_processes()
    button_stop_all_processes.on_click(on_click_stop_all_processes)

    list_hboxes.append(HBox([button_stop_all_processes], layout=HBOX_LAYOUT))
    #####
    list_hboxes.append(
        HBox(
            [ipywidgets.HTML("<h3>Choose process to show:</h3>")],
            layout=HBOX_LAYOUT)
    )
    BUTTONS_CHOOSE_PROCESS.options = list(
        process_manager_obj.dict_all_processes_by_id)
    list_hboxes.append(HBox([BUTTONS_CHOOSE_PROCESS], layout=HBOX_LAYOUT))
    BUTTONS_CHOOSE_PROCESS.observe(
        lambda _: update_one_process_choose_output(process_manager_obj),
        names='value')
    # # Choose which output to show
    update_one_process_choose_output(process_manager_obj)
    list_hboxes.append(VBOX_ONE_PROCESS_CHOOSE_OUTPUT)
    VBOX_CHOOSE_OUTPUT.children = list_hboxes


def create_jupyter_widget(process_manager_obj):
    """Create all widgets to interact with running processes

    Args:
        process_manager_obj (JupyterProcessesManager): Processes manager
    """
    list_hboxes_main = []
    # OUTPUT_PROCESSES_CONDITIONS
    list_hboxes_main.append(
        HBox([OUTPUT_PROCESSES_CONDITIONS], layout=HBOX_LAYOUT))
    # Choose which output to show
    create_choose_process(process_manager_obj)
    list_hboxes_main.append(VBOX_CHOOSE_OUTPUT)
    VBOX_MAIN_GUI.children = list_hboxes_main
    #####
    # Add output to application
    list_hboxes = [VBOX_MAIN_GUI]
    # Output to show
    list_hboxes.append(HBox([ipywidgets.HTML("<h2>Output:</h2>")]))
    list_hboxes.append(HBox([OUTPUT]))
    list_hboxes.append(HBox([ipywidgets.HTML("<br>")]))
    VBOX_APP_GUI.children = list_hboxes
    #####
    return VBOX_APP_GUI
