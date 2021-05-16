"""Module with functions to handle all ipywidget stuff"""
# Standard library imports
import os
import sys
import logging
from collections import OrderedDict
from time import sleep
import datetime

# Third party imports
import ipywidgets
from ipywidgets import HBox, VBox
from char import char
from IPython.display import clear_output
from IPython.display import display
from tqdm.auto import tqdm
from tabulate import tabulate
from yaspin import yaspin

# Local imports
from .class_one_process import OneProcess
from .other import timedelta_nice_format

MAIN_VBOX_LAYOUT = dict(
    # display="flex",
    width="100%",
    justify_content="center",
    align_self="center",
    # border='dashed 1px',
    padding="0px 0px 10px 0px"

)

HBOX_LAYOUT = dict(
    # display="flex", # Items will be put one after another
    flex_wrap="wrap",
        flex="1 1 auto",
    width="80%",
    justify_content="center",
    align_self="center",
)

VBOX_APP_GUI = ipywidgets.VBox()
VBOX_MAIN_GUI = ipywidgets.VBox(layout=MAIN_VBOX_LAYOUT)
VBOX_CHOOSE_OUTPUT = ipywidgets.VBox()

VBOX_CHOOSE_OUTPUT_TYPE = ipywidgets.VBox()

VBOX_ONE_PROCESS_CHOOSE_OUTPUT = ipywidgets.VBox()
OUTPUT_PROCESSES_CONDITIONS = ipywidgets.Output()
OUTPUT = ipywidgets.Output()
BUTTONS_CHOOSE_PROCESS = ipywidgets.ToggleButtons()
BUTTONS_CHOOSE_OUTPUT_TYPE = ipywidgets.ToggleButtons(
    options=["STDOUT", "STDERR"])
BUTTON_CLEAR_OUTPUT = ipywidgets.Button(
    description='clear',
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
)
WIDGET_LAST_LINES_TO_GET = ipywidgets.IntText(100)



# Create global events
BUTTON_CLEAR_OUTPUT.on_click(lambda _: OUTPUT.clear_output())
BUTTONS_CHOOSE_OUTPUT_TYPE.observe(
    lambda _:update_vbox_choose_output_type(), names='value')


def update_vbox_choose_output_type():
    """"""
    list_hboxes = []
    if BUTTONS_CHOOSE_OUTPUT_TYPE.value == "STDOUT":
        WIDGET_LAST_LINES_TO_GET.disabled = False
    else:
        WIDGET_LAST_LINES_TO_GET.disabled = True
    list_hboxes.append(HBox([
        ipywidgets.HTML("<h3>Choose output type:</h3>")],
        layout=HBOX_LAYOUT))
    list_hboxes.append(HBox([BUTTONS_CHOOSE_OUTPUT_TYPE], layout=HBOX_LAYOUT))
    wid_label = ipywidgets.Label("Last lines to get:")
    list_hboxes.append(
        HBox([wid_label, WIDGET_LAST_LINES_TO_GET], layout=HBOX_LAYOUT))
    VBOX_CHOOSE_OUTPUT_TYPE.children = list_hboxes




def update_one_process_choose_output(process_manager_obj):
    """"""
    list_hboxes = []

    update_vbox_choose_output_type()
    list_hboxes.append(VBOX_CHOOSE_OUTPUT_TYPE)


    int_chosen_process = BUTTONS_CHOOSE_PROCESS.value
    process_obj = process_manager_obj.dict_all_processes_by_id[int_chosen_process]




    button_show_output = ipywidgets.Button(
        description='Show output',
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    )
    list_hboxes.append(HBox([ipywidgets.HTML("<br>")]))
    list_hboxes.append(HBox(
        [button_show_output, BUTTON_CLEAR_OUTPUT], layout=HBOX_LAYOUT))

    def on_click(_):
        """"""
        OUTPUT.clear_output()
        if BUTTONS_CHOOSE_OUTPUT_TYPE.value == "STDOUT":
            str_output = process_obj.get_last_n_lines_of_stdout(
                int_last_lines=WIDGET_LAST_LINES_TO_GET.value)
        else:
            str_output = process_obj.get_last_error_msg()
        with OUTPUT:
            print(str_output)

    button_show_output.on_click(on_click)
    VBOX_ONE_PROCESS_CHOOSE_OUTPUT.children = list_hboxes


def create_choose_process(process_manager_obj):
    """"""
    list_hboxes = []

    list_hboxes.append(HBox([
        ipywidgets.HTML("<h3>Choose process to show:</h3>")],
        layout=HBOX_LAYOUT))
    BUTTONS_CHOOSE_PROCESS.options = list(
        process_manager_obj.dict_all_processes_by_id)
    list_hboxes.append(HBox([BUTTONS_CHOOSE_PROCESS], layout=HBOX_LAYOUT))
    BUTTONS_CHOOSE_PROCESS.observe(
        lambda _:update_one_process_choose_output(process_manager_obj), names='value')
    # # Choose which output to show
    update_one_process_choose_output(process_manager_obj)
    list_hboxes.append(VBOX_ONE_PROCESS_CHOOSE_OUTPUT)
    VBOX_CHOOSE_OUTPUT.children = list_hboxes


def create_jupyter_widget(process_manager_obj):
    """"""
    list_hboxes_main = []
    # OUTPUT_PROCESSES_CONDITIONS
    # list_hboxes_main.append(HBox([ipywidgets.HTML("<h2>Processes conditions:</h2>")], layout=HBOX_LAYOUT))
    list_hboxes_main.append(HBox([OUTPUT_PROCESSES_CONDITIONS], layout=HBOX_LAYOUT))
    # Choose which output to show
    create_choose_process(process_manager_obj)
    list_hboxes_main.append(VBOX_CHOOSE_OUTPUT)
    VBOX_MAIN_GUI.children = list_hboxes_main
    #####
    # Add output to application
    list_hboxes = [VBOX_MAIN_GUI]
    # Output to show
    # list_hboxes.append(HBox([ipywidgets.HTML("<hr>")], layout=HBOX_LAYOUT))
    # list_hboxes.append(HBox([ipywidgets.HTML("<hr>")], layout=HBOX_LAYOUT))
    # list_hboxes.append(HBox([ipywidgets.HTML("<hr>")], layout=HBOX_LAYOUT))
    list_hboxes.append(HBox([ipywidgets.HTML("<h2>Output:</h2>")]))
    list_hboxes.append(HBox([OUTPUT]))
    list_hboxes.append(HBox([ipywidgets.HTML("<br>")])) 
    VBOX_APP_GUI.children = list_hboxes
    #####
    return VBOX_APP_GUI
