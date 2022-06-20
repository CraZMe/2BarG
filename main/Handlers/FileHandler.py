import os
import numpy as np
from csv import reader as csv_reader
from easygui import fileopenbox, filesavebox
from pandas import read_excel


def select_data_file(signal_name, path, file_type):
    """
    In Thermal Analysis, the user chooses which file is which.
    'signal' can be INCID, TRANS, IR EXP, IR CAL or TC CAL.
    This function will use the selected file and rename it accordingly
    """
    os.chdir(path)  # Run cmd through the given path.
    file = fileopenbox()
    new_path = path + '/' + signal_name + "." + file_type

    os.rename(file, new_path)


def update_txt_file(data, filename, owd):
    os.chdir(owd)
    if not os.path.exists(owd+"/"+filename):
        f = open(filename, "x")
    else:
        f = open(filename, 'r+')

    f.truncate(0)
    s = ""
    for x in data:
        s += str(x[1]) + "\n"
    s += "\n"       # For some reason, there is a problem without a new line at the end of the defaults file.
    f.write(s)
    f.close()


def save_parameters_file(parameters):
    # Saves the current parameters (experiment_data, specimen_data ..).
    fname = filesavebox(default='2BarG_Parameter_Preset.main')
    if fname is not None:

        if not os.path.exists(fname):
            f = open(fname, "x")
        else:
            f = open(fname, 'r+')

        f.truncate(0)
        s = ""
        for x in parameters:
            s += str(x[1]) + "\n"
        s += "\n"  # For some reason, there is a problem without a new line at the end of the defaults file.
        f.write(s)
        f.close()


def load_parameters_file(parameters):
    fileName = fileopenbox()
    try:
        data = txt_to_array(fileName)
        if data != -1:
            for i in range(len(parameters)):
                parameters[i][1] = data[i]
    except:
        pass


def txt_to_array(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    succus = True
    for i in range(len(words)):
        try:
            words[i] = float(words[i])

        except Exception as e: print(e)

    if succus:
        return words
    else:
        return -1


def experiment_file_loader(file_type, exp_num, path_folder, thermal_analysis):
    if file_type == "csv" or file_type == "xlsx" or file_type == "txt" or file_type == "FLT":
        valid_files = True
    else:
        valid_files = False

    if valid_files:

        exp_path_incid = path_folder + "/Exp #" + str(exp_num) + "/" + file_type + "/incid." + file_type
        exp_path_trans = path_folder + "/Exp #" + str(exp_num) + "/" + file_type + "/trans." + file_type

        if thermal_analysis:
            exp_path_incid = path_folder + "/incid." + file_type
            exp_path_trans = path_folder + "/trans." + file_type
            exp_path_IR_EXP = path_folder + "/IR_EXP." + file_type
            exp_path_IR_CAL = path_folder + "/IR_CAL." + file_type
            exp_path_TC_CAL = path_folder + "/TC_CAL." + file_type

        if file_type == "FLT" or file_type == "txt":
            #   Incident
            vector_file = open(exp_path_incid)
            vector_incid = np.loadtxt(vector_file, delimiter='\t', skiprows=2)
            vector_file.close()

            # Transmitted
            vector_file = open(exp_path_trans)
            vector_trans = np.loadtxt(vector_file, delimiter='\t', skiprows=2)
            vector_file.close()

            if thermal_analysis:
                #   IR EXP
                vector_file = open(exp_path_IR_EXP)
                vector_IR_EXP = np.loadtxt(vector_file, delimiter='\t', skiprows=2)
                vector_file.close()

                # IR CAL
                vector_file = open(exp_path_IR_CAL)
                vector_IR_CAL = np.loadtxt(vector_file, delimiter='\t', skiprows=2)
                vector_file.close()

                # TC CAL
                vector_file = open(exp_path_TC_CAL)
                vector_TC_CAL = np.loadtxt(vector_file, delimiter='\t', skiprows=2)
                vector_file.close()

        elif file_type == "csv":
            vector_file = open(exp_path_incid)
            vector_csv = csv_reader(vector_file)
            vector_incid = []

            for row in vector_csv:
                vector_incid.append(row)
            vector_file.close()

            vector_file = open(exp_path_trans)
            vector_csv = csv_reader(vector_file)
            vector_trans = []
            for row in vector_csv:
                vector_trans.append(row)

            if thermal_analysis:
                vector_file = open(exp_path_IR_EXP)
                vector_csv = csv_reader(vector_file)
                vector_IR_EXP = []

                for row in vector_csv:
                    vector_IR_EXP.append(row)
                vector_file.close()

                vector_file = open(exp_path_IR_CAL)
                vector_csv = csv_reader(vector_file)
                vector_IR_CAL = []
                for row in vector_csv:
                    vector_IR_CAL.append(row)

                vector_file = open(exp_path_TC_CAL)
                vector_csv = csv_reader(vector_file)
                vector_TC_CAL = []
                for row in vector_csv:
                    vector_TC_CAL.append(row)

        elif file_type == "xlsx":
            vector_file = read_excel(exp_path_incid)
            vector_incid = vector_file.values

            vector_file = read_excel(exp_path_trans)
            vector_trans = vector_file.values

            if thermal_analysis:
                vector_file = read_excel(exp_path_IR_EXP)
                vector_IR_EXP = vector_file.values

                vector_file = read_excel(exp_path_IR_CAL)
                vector_IR_CAL = vector_file.values

                vector_file = read_excel(exp_path_TC_CAL)
                vector_TC_CAL = vector_file.values

        if thermal_analysis:
            return vector_incid, vector_trans, vector_IR_EXP, vector_IR_CAL, vector_TC_CAL

        return vector_incid, vector_trans, [],  [], []

    else:
        #   Files are not valid
        return [], [], [],  [], []
