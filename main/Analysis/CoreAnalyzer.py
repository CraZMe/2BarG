import numpy as np

import os

from scipy.integrate import trapz, cumtrapz

from main.Calculators import FinalCalculation
from main.Calculators.dispersion_correction import dispersion_correction
from main.Calculators.IR_calibration import IR_calibration
from main.Analysis import SignalProcessing
from main.Handlers import FileHandler

from main.Utilities.TwoDimVec import TwoDimVec


class CoreAnalyzer:

    def __init__(self, user_interface, path, mode, specimen_mode, thermal_analysis, parameters, spacing, smooth_value, bar_num, bridge_type):
        self.path_folder = path
        self.mode = mode
        self.specimen_mode = specimen_mode
        self.thermal_analysis = thermal_analysis
        self.parameters = parameters
        self.spacing = spacing
        self.smooth_value = smooth_value
        self.bar_num = bar_num
        self.user_interface = user_interface
        self.tpp = int
        self.exp_num = 1
        self.damp_f = 10 ** (-3)  # New variable to be used in the future (future...future......future...)
        self.bridge_type = bridge_type

        self.incid = TwoDimVec()
        self.trans = TwoDimVec()
        self.refle = TwoDimVec()

        self.corr_incid = TwoDimVec()
        self.corr_trans = TwoDimVec()
        self.corr_refle = TwoDimVec()

        self.incid_og = TwoDimVec()
        self.trans_og = TwoDimVec()

        self.incid_strain = None
        self.trans_strain = None

        self.IR_EXP = TwoDimVec()
        self.IR_CAL = TwoDimVec()
        self.TC_CAL = TwoDimVec()

    def configure_parameters(self, parameters, path_folder, poisson_ratio, prominence_percent, auto_open_report, smooth_value):
        """
            Configures all given parameters into the Signal Processing Class
        """
        self.user_interface.update_logger("Configuring Parameters...")
        self.path_folder = path_folder
        self.poisson_ratio = poisson_ratio

        self.spec_diam = float(parameters[0][1])
        self.specimen_length = float(parameters[1][1])
        self.bar_diameter = float(parameters[2][1])
        self.young_modulus = float(parameters[3][1])
        self.first_gage = float(parameters[4][1])
        self.second_gage = float(parameters[5][1])
        self.sound_velocity = float(parameters[6][1])
        self.gage_factor = float(parameters[7][1])
        self.bridge_tension = float(parameters[8][1])

        try:
            self.density = float(parameters[12][1])
            self.heat_capacity = float(parameters[13][1])

        except:
            self.user_interface.update_logger("Density & Heat Capacity not configured."
                  "Ignore this error for classic SHPB experiments (no thermal analysis).")

        self.prominence_percent = prominence_percent
        self.auto_open_report = auto_open_report
        self.smooth_value = smooth_value

    def load_experiments(self, exp_num, path_folder, mode, specimen_mode, file_type, thermal_analysis):
        """
            This function takes data from the loaded experiment and
            makes it into two voltage and two time vectors:
            incident & transmitted.

            It keeps an "og" version - an original version of the vectors
             to be untouched by any processing that follows.
        """
        self.user_interface.update_logger("Loading Experiments in Core Analyzer...")
        self.mode = mode
        self.specimen_mode = specimen_mode
        self.thermal_analysis = thermal_analysis
        self.exp_num = exp_num

        os.chdir(path_folder)  # Run cmd through the given path.
        self.user_interface.update_logger("...loading Files")
        incid, trans, IR_EXP, IR_CAL, TC_CAL = FileHandler.experiment_file_loader(file_type, exp_num, path_folder, thermal_analysis)
        self.user_interface.update_logger("...files loaded")
        self.incid = TwoDimVec([incid[i][1] for i in range(len(incid))],
                               [incid[i][0] for i in range(len(incid))]).force_signal_to_start_at_zero()
        self.trans = TwoDimVec([trans[i][1] for i in range(len(trans))],
                               [trans[i][0] for i in range(len(trans))]).force_signal_to_start_at_zero()

        if thermal_analysis:
            self.IR_EXP = TwoDimVec([IR_EXP[i][1] for i in range(len(IR_EXP))],
                                    [IR_EXP[i][0] for i in range(len(IR_EXP))]).force_signal_to_start_at_zero()
            self.IR_CAL = TwoDimVec([IR_CAL[i][1] for i in range(len(IR_CAL))],
                                    [IR_CAL[i][0] for i in range(len(IR_CAL))])
            self.TC_CAL = TwoDimVec([TC_CAL[i][1] for i in range(len(TC_CAL))],
                                    [TC_CAL[i][0] for i in range(len(TC_CAL))])

        # Extract Time Per Point from the data.
        self.tpp = self.incid.x[1] - self.incid.x[0]

        # og = original. the following are defined as the original signals taken directly from the FLT files.
        # Saving them is necessary for resetting the signal cropping.
        self.incid_og = self.incid_og.create_absolute_copy(self.incid)
        self.trans_og = self.trans_og.create_absolute_copy(self.trans)

        return True

    def analyze(self, purpose, exp_num, sp_mode, parameters, spacing, bar_num):
        """
            This function is the main function that calls all the
            processing and calculations done on the experiment files.

        purpose: Analyze one given experiment or all of the experiments
        sp_mode: Signal Proceesing mode: Manual / Automatic cropping
        return: True is analysis and report production was succusful, False otherwise.
        """
        self.spacing = spacing
        self.parameters = parameters
        if sp_mode == "Manual":
            """
                Manual cropping analysis
            """
            self.user_interface.update_logger("Manual Cropping CMPLT.")

            text = """Please Select 3 points: 
                   1) Incident's start, 2) Incident's end,  3) Reflected's start.
                    To delete the last selected point, press backspace. 
                    Once you are finished, please close this window."""

            x = SignalProcessing.manual_crop(self.incid_og.x, self.incid_og.y, text, "Incident")
            if x is None:
                #   If cropping process has been stopped by user or by program error, do nothing.
                return

            before_crop, after_crop, reflected_crop = float(x[0]), float(x[1]), float(x[2])

            text = """Please Select the Transmitted's starting point.
                    To delete the last selected point, press backspace.
                    Once you are finished, please close this window."""

            x = SignalProcessing.manual_crop(self.trans_og.x, self.trans_og.y, text, "Transmitted")
            if x is None:
                #   If cropping process has been stopped by user or by program error, do nothing.
                return

            #   we are only interested in the X point value (Time) for the signal cutting:
            transmitted_crop = float(x[0])

            SignalProcessing.crop_signal(self, "before", before_crop, None)
            SignalProcessing.crop_signal(self, "after", before_crop, after_crop)
            SignalProcessing.crop_signal(self, "reflected", before_crop, after_crop, reflected_crop)
            SignalProcessing.crop_signal(self, "transmitted", before_crop, after_crop, 0, transmitted_crop)

            if purpose == "single":
                #   analyze only one given experiment
                return self.single_analysis()

            elif purpose == "all":
                # Analyze all experiments
                return self.analyze_all()

        elif sp_mode == "Automatic":
            """
                Automatic cropping analysis
            """
            self.user_interface.update_logger("Automatic Cropping Initialized...")
            #   Analyze only one given experiment
            incid, trans, refle, IR_EXP, cropping_points = SignalProcessing.auto_crop(self.user_interface.update_logger, self)
            self.incid = self.incid.create_absolute_copy(incid)
            self.trans = self.trans.create_absolute_copy(trans)
            self.refle = self.refle.create_absolute_copy(refle)
            self.IR_EXP = self.IR_EXP.create_absolute_copy(IR_EXP)
            self.cropping_points = cropping_points
            return self.single_analysis()

    def single_analysis(self):
        corr_incident, corr_transmitted, corr_reflected = dispersion_correction(self.user_interface.update_logger, self)

        corr_incident, corr_transmitted, corr_reflected, \
        self.incid.x, self.trans.x, self.refle.x \
            = SignalProcessing.cross_correlate_signals(self.user_interface.update_logger, corr_incident, corr_transmitted,
                                                       corr_reflected,
                                                       self.incid.x, self.trans.x, self.refle.x,
                                                       self.smooth_value)
        self.corr_incid.y = corr_incident
        self.corr_trans.y = corr_transmitted
        self.corr_refle.y = corr_reflected

        valid = FinalCalculation.final_calculation(self.user_interface.update_logger, self)

        if valid:
            self.user_interface.update_logger("Analysis CMPLT.")
            from main.Handlers.OutputHandler import save_data
            self.user_interface.update_logger("Saving data...")
            save_data(self, self.exp_num, self.parameters, self.bar_num)
            self.user_interface.update_logger("Data Saved.")
            if self.thermal_analysis:
                from main.Handlers.OutputHandler import make_report_thermal
                make_report_thermal(self, self.exp_num, self.parameters, self.bar_num)
            else:
                from main.Handlers.OutputHandler import make_report
                make_report(self, self.exp_num, self.parameters, self.bar_num)

            return True

        return False

    def analyze_all(self):
        self.corr_incid.y, self.corr_trans.y, self.corr_refle.y = dispersion_correction(self.user_interface.update_logger, self)
        self.corr_incid.x = self.incid.x.copy()
        self.corr_trans.x = self.trans.x.copy()
        self.corr_refle.x = self.refle.x.copy()

        valid = FinalCalculation.final_calculation(self)
        if valid:
            return True
        else:
            return False
