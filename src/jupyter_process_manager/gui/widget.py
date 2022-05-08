"""Module with functions to handle all ipywidget stuff"""
from __future__ import print_function
# Standard library imports
import time
import threading

# Third party imports
import ipywidgets
from ipywidgets import HBox
from ipywidgets import VBox
from ipywidgets_toggle_buttons import ToggleButtonsAutoSize

# Local imports
from .layouts import MAIN_VBOX_LAYOUT
from .layouts import HBOX_LAYOUT


class WidgetProcessesManager(VBox):

    def __init__(self, process_manager_obj):
        """
        Widgets to interact with running processes

        Args:
            process_manager_obj (JupyterProcessesManager): Processes manager
        """
        super().__init__()
        self.process_manager_obj = process_manager_obj
        self.create_widget()

        threading.Thread(
            target=self._start_thread_auto_output_update,
            daemon=True,
        ).start()
        self._is_to_update_output = True

    def init_all_widgets(self):
        """"""
        self.OUTPUT_PROCESSES_CONDITIONS = ipywidgets.Output()
        self.OUTPUT = ipywidgets.Output()
        self.BUTTONS_CHOOSE_PROCESS = ToggleButtonsAutoSize()
        self.button_stop_all_processes = ipywidgets.Button(
            description='STOP ALL processes',
            button_style='warning',
            layout={"width": "200px"}
        )
        self.button_stop_all_processes.on_click(
            self._on_click_stop_all_processes)
        self.button_stop_process = ipywidgets.Button(
            description='STOP NONE process',
            button_style='warning',
            layout={"width": "200px"}
        )
        self.togbut_select_what_to_show = ToggleButtonsAutoSize(
            options=["Show process STDOUT", "Show LAST ERROR", "Show ALL ERRORs"])
        self.togbut_select_what_to_show.observe(
            self._update_output, names='value')
        self.button_update = ipywidgets.Button(
            description='FORCE UPDATE',
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            layout={"width": "200px"}
        )
        self.button_update.on_click(self._update_output)
        self.HBOX_BUTTONS_CHOOSE_OUTPUT = HBox(layout=HBOX_LAYOUT)
        self.VBOX_CHOOSE_PROCESS = VBox()
        self.VBOX_MAIN_GUI = VBox(layout=MAIN_VBOX_LAYOUT)



    def create_widget(self):
        """"""
        self.init_all_widgets()
        # Main GUI
        self.create_vbox_main_gui()
        list_hboxes = [self.VBOX_MAIN_GUI]
        # Output to show
        list_hboxes.append(HBox([ipywidgets.HTML("<h2>Output:</h2>")]))
        list_hboxes.append(HBox([self.OUTPUT]))
        list_hboxes.append(HBox([ipywidgets.HTML("<br>")]))
        self.children = list_hboxes
        self.update_widget()


    def create_vbox_main_gui(self):
        """"""
        list_hboxes_main = []
        # OUTPUT_PROCESSES_CONDITIONS
        list_hboxes_main.append(
            HBox([self.OUTPUT_PROCESSES_CONDITIONS], layout=HBOX_LAYOUT))
        # Choose which output to show
        self._create_vbox_choose_process()
        list_hboxes_main.append(self.VBOX_CHOOSE_PROCESS)
        # Stop ALL Processes
        list_hboxes_main.append(
            HBox([self.button_stop_process, self.button_stop_all_processes],
            layout=HBOX_LAYOUT))
        list_hboxes_main.append(
            HBox(
                [ipywidgets.HTML("<h3>Select what to show:</h3>")],
                layout=HBOX_LAYOUT)
        )
        list_hboxes_main.append(
            HBox([self.togbut_select_what_to_show],
            layout=HBOX_LAYOUT))

        list_hboxes_main.append(
            HBox([self.button_update],
            layout=HBOX_LAYOUT))

        self.VBOX_MAIN_GUI.children = list_hboxes_main

    def update_widget(self):
        """"""
        self.update_choose_process()
        self.update_button_process_to_stop()

    def update_choose_process(self, *_):
        """"""
        self.BUTTONS_CHOOSE_PROCESS.options = list(
            self.process_manager_obj.dict_all_processes_by_id)
        self.BUTTONS_CHOOSE_PROCESS.observe(
            self.update_button_process_to_stop, names='value')
        self.BUTTONS_CHOOSE_PROCESS.observe(
            self._update_output, names='value')

    def update_button_process_to_stop(self, *_):
        """"""
        self.button_stop_process._click_handlers.callbacks = []
        int_chosen_process = self.BUTTONS_CHOOSE_PROCESS.value
        if int_chosen_process is None:
            return None
        process_obj = \
            self.process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        self.button_stop_process.description = \
            f'STOP {int_chosen_process} process'
        if process_obj.is_alive():
            self.button_stop_process.disabled = False
            self.button_stop_process.on_click(self._on_click_stop_process)
            self._is_to_update_output = True
        else:
            self.button_stop_process.disabled = True

    def _create_vbox_choose_process(self):
        """Create all widgets starting from choose process
        """
        list_hboxes = []
        list_hboxes.append(
            HBox(
                [ipywidgets.HTML("<h3>Select process:</h3>")],
                layout=HBOX_LAYOUT)
        )
        list_hboxes.append(
            HBox([self.BUTTONS_CHOOSE_PROCESS], layout=HBOX_LAYOUT))
        self.VBOX_CHOOSE_PROCESS.children = list_hboxes

    def _update_output(self, *_, clear_output_at_first=True):
        """"""
        if clear_output_at_first:
            self.OUTPUT.clear_output(wait=True)
        output_type = self.togbut_select_what_to_show.value
        if output_type == "Show process STDOUT":
            self._show_stdout()
        elif output_type == "Show LAST ERROR":
            self._show_last_error()
        elif output_type == "Show ALL ERRORs":
            self._show_all_errors()
        else:
            raise ValueError(f"Wrong value of output type: {output_type}")

    def _on_click_stop_all_processes(self, *_):
        """"""
        self.OUTPUT.clear_output(wait=True)
        with self.OUTPUT:
            self.process_manager_obj.terminate_all_alive_processes()
            print("=" * 79)
        self._update_output(clear_output_at_first=False)
        self.update_button_process_to_stop()
        self._is_to_update_output = False

    def _on_click_stop_process(self, _):
        """"""
        self._is_to_update_output = False
        self.OUTPUT.clear_output(wait=True)
        int_chosen_process = self.BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            self.process_manager_obj.dict_all_processes_by_id[int_chosen_process]

        with self.OUTPUT:
            print("Stopping process: ", int_chosen_process)
            process_obj.terminate()
            print("---> Done. Process %d TERMINATED" % int_chosen_process)
            print("=" * 79)

        self._update_output(clear_output_at_first=False)
        self.update_button_process_to_stop()
        # self._is_to_update_output = False

    def _show_stdout(self, *_):
        """"""
        int_chosen_process = self.BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            self.process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        str_output = process_obj.get_stdout()
        with self.OUTPUT:
            print("STDOUT:")
            print(str_output)

    def _show_last_error(self, *_):
        """"""
        int_chosen_process = self.BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            self.process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        int_errors_happened = len(process_obj.get_list_all_errors())
        with self.OUTPUT:
            print("Last Error:")
            print("ERRORs found: ", int_errors_happened)
            if int_errors_happened:
                str_last_error = process_obj.get_last_error_msg()
                print("Last error message: ")
                print(str_last_error)

    def _show_all_errors(self, *_):
        """"""
        int_chosen_process = self.BUTTONS_CHOOSE_PROCESS.value
        process_obj = \
            self.process_manager_obj.dict_all_processes_by_id[int_chosen_process]
        all_errors = process_obj.get_list_all_errors()
        with self.OUTPUT:
            print("All Errors:")
            print("ERRORs found: ", len(all_errors))
            for error_num, error_text in enumerate(all_errors):
                print("=" * 79)
                print("ERROR:", error_num)
                print(error_text)


    def _start_thread_auto_output_update(self):
        """"""
        while True:
            time.sleep(1)
            self.OUTPUT_PROCESSES_CONDITIONS.clear_output(wait=True)
            with self.OUTPUT_PROCESSES_CONDITIONS:
                self.process_manager_obj.print_info_about_running_processes(
                    int_max_processes_to_show=10)
            time.sleep(1)
            if self._is_to_update_output:
                self._update_output(clear_output_at_first=True)
