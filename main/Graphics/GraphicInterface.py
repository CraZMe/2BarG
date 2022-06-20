from kivymd.uix.list import OneLineListItem

import main.Graphics.GuiTabsKV as tabs

from main.Handlers import FileHandler
from main.Handlers import PathHandler
from main.Analysis import CoreAnalyzer

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.core.window import Window

import os


class InfoTab(MDFloatLayout, MDTabsBase):
    pass


class ParametersTab(MDFloatLayout, MDTabsBase):
    pass


class SettingsTab(MDFloatLayout, MDTabsBase):
    pass


class MyToggleButton(MDRaisedButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_down = "#607262"
        self.md_bg_color = (0.95, 0.88, 0.82, 1)
        self.background_normal = "#f4e3d1"


class HoverTextButton(HoverBehavior, MDTextButton):
    pass


class UserInterface(MDApp):

    def __init__(self, **kwargs):
        super().__init__()
        # of experiment: Compression or Tension (1 or -1 respectively).
        # Most experiments are Compression experiments, so the default will be 1.
        # This variable will change when pressing on the Compression (C) or Tension (T) buttons in the program.

        self.owd = os.getcwd()  # Original working directory
        self.poisson_ratio = 0.33
        self.mode = "compression"
        self.specimen_mode = "regular"
        self.num_of_experiments = 0
        self.bar_num = 2
        self.spacing = None
        self.smooth_value = None
        self.bridge_type = 0.25

        # Get the current (original) directory for os operations.  This string will be valuable when using
        # the "Change Path Folder" button. Used in arrange_files_in_path function.
        self.two_bar_g_path = os.getcwd()

        #   define default path input
        self.path_folder = ""

        #   This function will create a matrix called "parameters",
        #   as well as define some needed variables.
        self.set_data()

        #   In the Parameters Menu, there is a dropdown bar to choose an experiment.
        #   This new list (experiment_menu_items) will contain the experiments.
        if not self.thermal_analysis:
            self.experiment_menu_items = [{"text": f"No Experiments Loaded",
                                        "viewclass": "OneLineListItem", "height": dp(54)}]
        else:
            self.experiment_menu_items = []

        self.CA = CoreAnalyzer.CoreAnalyzer(self, self.path_folder, self.mode, self.specimen_mode,
                                            self.thermal_analysis, self.parameters,
                                            self.spacing, self.smooth_value, self.bar_num,
                                            self.bridge_type)

        #   Cropping mode is set to automatic as default:
        self.sp_mode = "Automatic"
        self.auto_open_report = True

        #   Defines the spacing, prominence and Curve Smoothing values used in the signal processing algorithms.
        self.spacing = 60
        self.prominence_percent = 0.5
        self.smooth_value = 71
        self.about_dfl = "The Mechanics and Physics of high rate deformation and fracture is the central and historical research theme" \
                         " of the Dynamic Fracture Laboratory (DFL). The DFL was started within the Materials Mechanics Center in 1994" \
                         " by D. Rittel, to address specific issues in dynamic fracture mechanics and stress wave physics through a" \
                         " combined experimental-numerical approach." \
                         "\n\n" \
                         "Since then, the Dynamic Fracture Laboratory has been actively developing new tools and techniques to address" \
                         " these issues, while expanding its activity to other related and exciting new domains, such as soft matter" \
                         " mechanics and dental biomechanics, or dental engineering. Throughout our research, we never lose sight of" \
                         " the governing physics of the processes that we characterize and model."

        self.guide = """1. Using the "Set Path Folder" button, choose the folder you stored your experiment files at. The files should be numbered.
        2. Fill in the experiment's parameters on the left. Make sure to press Enter each time you enter a new value. 
        3. Choose your experiment mode (compression / tension) and your cropping mode (automatic or manual). 
        4. Choose which experiment to analyse using the "Choose Experiment button", or analyse all of them.
        """

        self.logger_text = "2BarG Initialized."

    def set_data(self):
        """
            A simple function that groups all needed values to the "parameters" matrix and creates
            some variables that is needed for the control of the program.
        """
        data = FileHandler.txt_to_array("ProgramFiles/defaults.TwoBarG")
        spec_diam = data[0]
        spec_length = data[1]
        bar_diameter = data[2]
        young_modulus = data[3]
        first_gage = data[4]
        second_gage = data[5]
        sound_velocity = data[6]
        gage_factor = data[7]
        bridge_tension = data[8]

        lod = data[10]
        if data[11] == "True":
            self.thermal_analysis = True
        if data[11] == "False":
            self.thermal_analysis = False
        density = data[12]
        heat_capacity = data[13]
        if data[14] == "True":
            quarter = True
        else:
            quarter = False

        if data[15] == "True":
            half = True
        else:
            half = False

        if data[16] == "True":
            full = True
        else:
            full = False

        self.parameters = [["Specimen Diameter", spec_diam],
                           ["Specimen Length", spec_length],
                           ["Bar Diameter", bar_diameter],
                           ["Young's Modulus", young_modulus],
                           ["First Gauge", first_gage],
                           ["Second Gauge", second_gage],
                           ["Sound Velocity", sound_velocity],
                           ["Gauge Factor", gage_factor],
                           ["Bridge Tension", bridge_tension],
                           ["Path", self.path_folder],
                           ["Light or Dark", lod],
                           ["Thermal Analysis", self.thermal_analysis],
                           ["Density", density],
                           ["Heat Capacity", heat_capacity],
                           ["Quarter", quarter],
                           ["Half", half],
                           ["Full", full]]

        #   lod = Light Or Dark
        if lod == "Dark":
            self.light_or_dark = (0.2, 0.2, 0.2, 1)
            self.theme_cls.theme_style = "Dark"

        else:
            self.light_or_dark = (0.98, 0.976, 0.957, 1)

    def build(self):
        """
            This functions builds the actual GUI, and most of it is graphic configuration of themes, buttons and screens.
        """
        # Set color themes and colors:

        self.theme_cls.primary_palette = "Red"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_hue = "A100"
        self.main_color = "#607262"
        self.pink = "#e5b9b0"
        self.beige = "#f4e3d1"
        self.white = "#faf9f4"

        self.text_font = "GOTHIC"

        self.icon = "2BarG_emblem.ico"

        Window.bind(on_request_close=self.on_request_close)

        return Builder.load_string(tabs.Tabs)

    def on_start(self):

        # Add the different Tabs
        self.root.ids.tabs.add_widget(InfoTab(title="INFO"))
        self.root.ids.tabs.add_widget(ParametersTab(title="PARAMETERS"))
        self.root.ids.tabs.add_widget(SettingsTab(title="SETTINGS"))

        # Make the startup tab the Main Tab
        self.root.ids.tabs.switch_tab("PARAMETERS", search_by="title")

        # Define the experiments menu items (in Signal Processing tab)
        self.experiments_menu = MDDropdownMenu(caller=self.root.ids.tabs.get_slides()[1].ids.experiment_chooser,
                                               items=self.experiment_menu_items,
                                               width_mult=3)

        if self.light_or_dark == (0.2, 0.2, 0.2, 1):
            self.root.ids.tabs.get_slides()[2].ids.dark_mode.active = True

        if self.thermal_analysis:
            self.root.ids.tabs.get_slides()[2].ids.thermal_analysis.active = True

        self.root.ids.tabs.get_slides()[2].ids.quarter.active = self.parameters[14][1]
        self.root.ids.tabs.get_slides()[2].ids.half.active = self.parameters[15][1]
        self.root.ids.tabs.get_slides()[2].ids.full.active = self.parameters[16][1]

        self.set_path_folder(self.path_folder)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        instance_tab.ids.label = instance_tab_label

    def use_experiment(self, exp_num):
        # When an experiment is choosen, new buttons will appear, this function defines them.
        instance_text = "Experiment " + str(exp_num)
        if self.num_of_experiments != 0:
            # Dismiss the dropdown menu.
            self.experiments_menu.dismiss()

            #   Start analysis process:
            self.call_CA_analyze(exp_num, "single")

    def call_CA_analyze(self, exp_num, purpose):
        """
            Calls Signal Processing's "analyze" function after
            loading the files and checking they are valid for use.

            purpose:        Analyze one experiment or all of them.
            returns nothing.
        """
        #   Get current smooth value from slider on settings tab:
        self.smooth_value = self.root.ids.tabs.get_slides()[2].ids.smooth_slider.value

        try:
            # load the experiment files and check if they are valid for further analysis:
            valid_files = self.CA.load_experiments(exp_num,
                                                   self.path_folder,
                                                   self.mode,
                                                   self.specimen_mode,
                                                   self.file_type,
                                                   self.thermal_analysis)

            if valid_files:
                try:
                    self.CA.configure_parameters(self.parameters,
                                                 self.path_folder,
                                                 self.poisson_ratio,
                                                 self.prominence_percent,
                                                 self.auto_open_report,
                                                 self.smooth_value)
                except:
                    self.update_logger("Parameter configuration FAILED.")
                    self.error_message()

                #   Analyze experiment files:
                valid = self.CA.analyze(purpose, exp_num, self.sp_mode, self.parameters, self.spacing, self.bar_num)

                if not valid:
                    self.update_logger("Analysis Failed")
                    self.error_message()

            else:
                self.update_logger("\nLoaded files are not valid.")
                self.error_message()

        except Exception as e:
            self.update_logger("Something went wrong: \n")
            self.update_logger(str(e))
            self.error_message()

    def analyse_all_experiments(self):
        self.CA.configure_parameters(self.parameters,
                                     self.path_folder,
                                     self.poisson_ratio,
                                     self.prominence_percent,
                                     self.auto_open_report,
                                     self.smooth_value)

        if self.num_of_experiments > 1:
            errors = []

            for i in range(self.num_of_experiments):

                try:
                    self.CA.load_experiments(i + 1, self.path_folder, self.mode, self.specimen_mode, self.file_type, self.thermal_analysis)
                    valid = self.CA.analyze("all", i + 1, self.sp_mode, self.parameters, self.spacing, self.bar_num)
                    if not valid:
                        errors.append(i + 1)
                except Exception as e:
                    errors.append(i + 1)
                    self.update_logger("\n" + str(e))

            if len(errors) != 0:
                # open a dialog if some experiments were corrupt.
                text = "There seem to be some problems with the following experiments: \n" \
                       + (" " * (26 // len(errors))) + str(errors).strip('[]') + "\n" \
                                                                                 "Please make sure that: \n\n" \
                                                                                 "¤   Your file type is supported\n" \
                                                                                 "¤   The correct mode is selected \n" \
                                                                                 "¤   All parameters are valid\n"

                dialog = MDDialog(title="Some experiments didn't make it.",
                                  text=text,
                                  size_hint=(0.26, 1),
                                  radius=[20, 7, 20, 7])
                dialog.open()

        else:
            self.call_CA_analyze(1, "single")

    def error_message(self, text=""):
        """
        Opens the "Something went wrong" popup.
        """
        if text == "":
            text = "Please make sure that: \n\n" \
               "¤   Path folder is empty of \n" \
               "      irrelevant files.\n" \
               "¤   Your file type is supported\n" \
               "¤   The correct mode is selected \n" \
               "¤   All parameters are valid\n" \
               "¤   Curve smoothing is \n" \
               "      appropriate\n" \


        dialog = MDDialog(title='Something went wrong.',
                          text=text,
                          size_hint=(0.3, 1),
                          radius=[20, 7, 20, 7])
        dialog.open()

    def on_request_close(self, *args):
        self.stop()

    def removes_marks_all_chips(self, selected_instance_chip):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    def set_path_folder(self, path):
        self.path_folder = path
        self.parameters[9][1] = path

        if path != "":
            if self.thermal_analysis:
                #   If thermal analysis is desired, use the corresponding function for setting the path input.
                self.num_of_experiments, self.file_type = PathHandler.set_path_input_thermal(self.path_folder, self.two_bar_g_path)

            else:
                num_of_experiments, self.file_type = PathHandler.set_path_input(self.path_folder, self.two_bar_g_path, self.thermal_analysis)

                if num_of_experiments != 0:
                    # If the number of experiments is 0 (aka there are no experiments loaded),
                    # there is no reason to reconfigure the Drop - Down Choose Experiment menu.
                    # Configure the "Choose Experiment" button's menu items.
                    self.num_of_experiments = num_of_experiments
                    self.experiment_menu_items = [{
                        "text": f"Experiment {i + 1}",
                        "viewclass": "OneLineListItem", "height": dp(54),
                        "on_release": lambda x=i + 1: self.use_experiment(x),
                    } for i in range(num_of_experiments)]

                elif num_of_experiments == 0:
                    self.experiment_menu_items = [{"icon": "flask",
                                                   "text": "No Experiments Loaded",
                                                   "viewclass": "OneLineListItem",
                                                   "height": dp(54)}]

                # Configure the menu itself.
                self.experiments_menu = MDDropdownMenu(caller=self.root.ids.tabs.get_slides()[1].ids.experiment_chooser,
                                                       items=self.experiment_menu_items,
                                                       pos_hint={"center_x": .5, "center_y": .5},
                                                       width_mult=2.1)

                #   Configure the needed parameters in the SignalProcessing class.
                self.CA.configure_parameters(self.parameters,
                                             self.path_folder,
                                             self.poisson_ratio,
                                             self.prominence_percent,
                                             self.auto_open_report,
                                             self.smooth_value)

    def update_logger(self, text):
        new_log = OneLineListItem(text=text, font_style='Caption', on_release=lambda _: self.show_log_dialog(text))
        self.root.ids.tabs.get_slides()[2].ids.logger_list.add_widget(new_log)

    def show_log_dialog(self, text):
        dialog = MDDialog(title='Expanded Logger Message:',
                          text=text,
                          size_hint=(0.4, 1),
                          radius=[20, 7, 20, 7])
        dialog.open()

    def ButtonAction_set_path_folder(self):
        path = PathHandler.choose_path()
        try:
            if path is not None:
                self.set_path_folder(path)
        except:
            self.error_message()

    def ButtonAction_select_data_file(self, signal_name):
        try:
            FileHandler.select_data_file(signal_name, self.path_folder, self.file_type)
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_save_parameters_file(self):
        try:
            FileHandler.save_parameters_file(self.parameters)
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_update_parameter(self, data_type, parameter_index, instance):
        #   Update the parameter of given text field.
        #   "instance" is the text field itself from the Parameters tab.
        try:
            if instance.text != '' and instance.text != " ":
                if data_type == "experiment" or data_type == "specimen":
                    if parameter_index == 3:
                        #   Index 3 is Young Modulus, which is given in Giga - Pascals:
                        self.parameters[parameter_index][1] = float(instance.text) * (10 ** 9)
                    else:
                        self.parameters[parameter_index][1] = float(instance.text)

                if data_type == "spacing":
                    self.spacing = int(round(float(instance.text)))

                if data_type == "prominence":
                    self.prominence_percent = int(round(float(instance.text))) / 100
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_set_parameters_as_default(self):
        # Saves the current parameters (experiment_data, specimen_data ..) in the defaults file.
        try:
            FileHandler.update_txt_file(self.parameters, "ProgramFiles/defaults.TwoBarG", self.owd)
            self.root.ids.tabs.get_slides()[1].ids.spec_diam.helper_text = "Default value: {}".format(self.parameters[0][1])
            self.root.ids.tabs.get_slides()[1].ids.spec_length.helper_text = "Default value: {}".format(
                self.parameters[1][1])
            self.root.ids.tabs.get_slides()[1].ids.bar_diameter.helper_text = "Default value: {}".format(
                self.parameters[2][1])
            self.root.ids.tabs.get_slides()[1].ids.young_modulus.helper_text = "Default value: {}".format(
                self.parameters[3][1] / 1e9)
            self.root.ids.tabs.get_slides()[1].ids.first_gage.helper_text = "Default value: {}".format(
                self.parameters[4][1])
            self.root.ids.tabs.get_slides()[1].ids.second_gage.helper_text = "Default value: {}".format(
                self.parameters[5][1])
            self.root.ids.tabs.get_slides()[1].ids.sound_velocity.helper_text = "Default value: {}".format(
                self.parameters[6][1])
            self.root.ids.tabs.get_slides()[1].ids.gage_factor.helper_text = "Default value: {}".format(
                self.parameters[7][1])
            self.root.ids.tabs.get_slides()[1].ids.bridge_tension.helper_text = "Default value: {}".format(
                self.parameters[8][1])
            self.root.ids.tabs.get_slides()[2].ids.density.helper_text = "Default value: {}".format(
                self.parameters[12][1])
            self.root.ids.tabs.get_slides()[2].ids.heat_capacity.helper_text = "Default value: {}".format(
                self.parameters[13][1])
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_change_auto_open_report(self):
        if not self.auto_open_report:
            self.auto_open_report = True
        else:
            self.auto_open_report = False

    def ButtonAction_load_parameters_file(self):
        try:
            FileHandler.load_parameters_file(self.parameters)
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_show_data(self):
        #   opens a dialog with the current parameters.
        #   dialog_text = "\nDefault Path = " + self.path_folder
        try:
            dialog_text = "\n"
            dialog_text += str(self.parameters[0][0]) + " = " + str(self.parameters[0][1] * 1e3) + " [mm]" + "\n"
            dialog_text += str(self.parameters[1][0]) + " = " + str(self.parameters[1][1] * 1e3) + " [mm]" + "\n"
            dialog_text += str(self.parameters[2][0]) + " = " + str(self.parameters[2][1] * 1e3) + " [mm]" + "\n"
            dialog_text += str(self.parameters[3][0]) + " = " + str(self.parameters[3][1] * 1e-9) + " [GPa]" + "\n"
            dialog_text += str(self.parameters[4][0]) + " = " + str(self.parameters[4][1]) + " [m]" + "\n"
            dialog_text += str(self.parameters[5][0]) + " = " + str(self.parameters[5][1]) + " [m]" + "\n"
            dialog_text += str(self.parameters[6][0]) + " = " + str(self.parameters[6][1]) + " [m/s]" + "\n"
            dialog_text += str(self.parameters[7][0]) + " = " + str(self.parameters[7][1]) + "\n"
            dialog_text += str(self.parameters[8][0]) + " = " + str(self.parameters[8][1]) + " [V]" + "\n\n"

            self.tap_target_view = MDTapTargetView(
                widget=self.root.ids.tabs.get_slides()[1].ids.show_parameters,
                title_text="Current Parameters",
                title_text_size="30sp",
                description_text=dialog_text,
                description_text_size="18sp",
                outer_circle_color=(0.898, 0.725, 0.69),
                title_text_color=(0.376, 0.447, 0.38, 1),
                description_text_color=(0.376, 0.447, 0.38, 1),
                widget_position="right",
                outer_radius=dp(290),
                cancelable=True,
            )

            if self.tap_target_view.state == "close":
                self.tap_target_view.start()
            else:
                self.tap_target_view.stop()
        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_change_bar_num(self):
        if self.bar_num == 1:
            self.bar_num = 2
        else:
            self.bar_num = 1

    def ButtonAction_change_thermal_analysis(self):
        try:
            active = self.root.ids.tabs.get_slides()[2].ids.thermal_analysis.active

            if active:
                self.thermal_analysis = True
                #   Replace the "Analyze." button's function to directly analyze the only experiment that's loaded.
                #   (in Thermal Analysis only one experiment is loaded at a time).
                self.root.ids.tabs.get_slides()[1].ids.experiment_chooser.on_release = lambda: self.use_experiment(1)
                self.experiments_menu.items = []
                #   Make the Thermal Analysis buttons visible & active:
                self.root.ids.tabs.get_slides()[1].ids.INCID.disabled = False
                self.root.ids.tabs.get_slides()[1].ids.INCID.opacity = 1
                self.root.ids.tabs.get_slides()[1].ids.TRANS.disabled = False
                self.root.ids.tabs.get_slides()[1].ids.TRANS.opacity = 1
                self.root.ids.tabs.get_slides()[1].ids.IR_EXP.disabled = False
                self.root.ids.tabs.get_slides()[1].ids.IR_EXP.opacity = 1
                self.root.ids.tabs.get_slides()[1].ids.IR_CAL.disabled = False
                self.root.ids.tabs.get_slides()[1].ids.IR_CAL.opacity = 1
                self.root.ids.tabs.get_slides()[1].ids.TC_CAL.disabled = False
                self.root.ids.tabs.get_slides()[1].ids.TC_CAL.opacity = 1
                self.root.ids.tabs.get_slides()[2].ids.density.disabled = False
                self.root.ids.tabs.get_slides()[2].ids.density.opacity = 1
                self.root.ids.tabs.get_slides()[2].ids.heat_capacity.disabled = False
                self.root.ids.tabs.get_slides()[2].ids.heat_capacity.opacity = 1

            else:
                self.thermal_analysis = False
                self.root.ids.tabs.get_slides()[1].ids.experiment_chooser.on_release = lambda: self.experiments_menu.open()
                self.experiments_menu.items = self.experiment_menu_items
                #   Make the Thermal Analysis buttons invisible & deactivated:
                self.root.ids.tabs.get_slides()[1].ids.INCID.disabled = True
                self.root.ids.tabs.get_slides()[1].ids.INCID.opacity = 0
                self.root.ids.tabs.get_slides()[1].ids.TRANS.disabled = True
                self.root.ids.tabs.get_slides()[1].ids.TRANS.opacity = 0
                self.root.ids.tabs.get_slides()[1].ids.IR_EXP.disabled = True
                self.root.ids.tabs.get_slides()[1].ids.IR_EXP.opacity = 0
                self.root.ids.tabs.get_slides()[1].ids.IR_CAL.disabled = True
                self.root.ids.tabs.get_slides()[1].ids.IR_CAL.opacity = 0
                self.root.ids.tabs.get_slides()[1].ids.TC_CAL.disabled = True
                self.root.ids.tabs.get_slides()[1].ids.TC_CAL.opacity = 0
                self.root.ids.tabs.get_slides()[2].ids.density.disabled = True
                self.root.ids.tabs.get_slides()[2].ids.density.opacity = 0
                self.root.ids.tabs.get_slides()[2].ids.heat_capacity.disabled = True
                self.root.ids.tabs.get_slides()[2].ids.heat_capacity.opacity = 0

            self.parameters[11][1] = self.thermal_analysis
            FileHandler.update_txt_file(self.parameters, "ProgramFiles/defaults.TwoBarG", self.owd)

        except Exception as e:
            self.update_logger(str(e))

    def ButtonAction_change_theme(self):
        active = self.root.ids.tabs.get_slides()[2].ids.dark_mode.active
        if active:
            self.theme_cls.theme_style = "Dark"
            self.light_or_dark = (0.2, 0.2, 0.2, 1)
            tab_list = self.root.ids.tabs.get_slides()
            tab_list[0].add_widget(Image(source="images/2BarG_white.png", pos_hint={"center_x": 0.5, "center_y": 0.8}))

            self.parameters[10][1] = "Dark"

        else:
            self.theme_cls.theme_style = "Light"
            self.light_or_dark = (0.98, 0.976, 0.957, 1)
            tab_list = self.root.ids.tabs.get_slides()
            tab_list[0].add_widget(Image(source="images/2BarG.png", pos_hint={"center_x": 0.5, "center_y": 0.8}))

            self.parameters[10][1] = "Light"

        for i in range(3):
            tab_list[i].md_bg_color = self.light_or_dark

        FileHandler.update_txt_file(self.parameters, "ProgramFiles/defaults.TwoBarG", self.owd)

    def ButtonAction_open_curve_smoothing_dialog(self):
        dialog_text = """
            A filter (smoothing) is applied on 
            a separate copy of the raw signals.
            This is done to filter out experiment
            noises and get a better estimate
            of the signal's peaks. 

            The "Curve Smoothing" parameter 
            is the "window length" when 
            applying a Savitzky-Golay filter 
            upon the raw signals. 

            As a rule of thumb:
            the higher the window length,
            the smoother the signal. 

            """

        self.curve_smoothing_tap_target = MDTapTargetView(
            widget=self.root.ids.tabs.get_slides()[2].ids.curve_smooth_info,
            title_text="       Curve Smoothing",
            title_text_size="30sp",
            description_text=dialog_text,
            description_text_size="18sp",
            title_text_color=(0.376, 0.447, 0.38, 1),
            description_text_color=(0.376, 0.447, 0.38, 1),
            widget_position="top",
            target_radius=dp(0),
            outer_radius=dp(0),
            cancelable=True,
        )

        if self.curve_smoothing_tap_target.state == "close":
            self.curve_smoothing_tap_target.start()
        else:
            self.curve_smoothing_tap_target.stop()

    def toggle_view_logger(self):
        if self.root.ids.tabs.get_slides()[2].ids.logger_card.opacity == 1:
            self.root.ids.tabs.get_slides()[2].ids.logger_card.opacity = 0
        else:
            self.root.ids.tabs.get_slides()[2].ids.logger_card.opacity = 1

    def set_bridge_type(self, value):
        self.CA.bridge_type = value
        self.parameters[14][1] = self.root.ids.tabs.get_slides()[2].ids.quarter.active
        self.parameters[15][1] = self.root.ids.tabs.get_slides()[2].ids.half.active
        self.parameters[16][1] = self.root.ids.tabs.get_slides()[2].ids.full.active
        FileHandler.update_txt_file(self.parameters, "ProgramFiles/defaults.TwoBarG", self.owd)


