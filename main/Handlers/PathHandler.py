import os
import shutil

from easygui import diropenbox


def set_path_input(path, two_bar_g_path, thermal_analysis):
    """
        This functions uses the chosen (or default) path given to the main program to do the following:
        The path folder chosen shall be one with raw experiment data in 'WFT' files,
        if this condition is not satisfied then this function will do nothing (can also mean that this function
        has already ran in the given path).
        If it is satisfied, then this function will convert the WFT files into FLT files using WFT2FLT.EXE
        and sort everything into experiments, divided by folders (EXP #1, EXP #2 ..)
        After everything is sorted, this function will create
        a dropdown menu of experiments in the Signal Processing menu, for further usage.
    """
    if thermal_analysis:
        set_path_input_thermal(path, two_bar_g_path)
    else:
        if path != "" and os.path.isdir(path):
            try:
                os.chdir(path)  # Run cmd through the given path.
                files = os.listdir(path)  # make a list of file names from the path directory

                '''
                    The following loop will check if the data files are in WFT format.
                    If so, a conversion to FLT file type will be made using the WFT2FLT.EXE program.   
                '''

                apply_WFT2FLT = False
                for file in files:
                    file_name, file_type = os.path.splitext(file)
                    file_type = file_type[1:]

                    if file_type == "WFT":
                        apply_WFT2FLT = True
                        break

                if "Exp #1" not in files:
                    # If there is at least one experiment folder then the
                    # WFT2FLT program has already been executed before,
                    # and there is no need to run it again.
                    # This condition can save startup time.

                    os.chdir(two_bar_g_path)  # Run cmd from this program's (main) path.

                    if apply_WFT2FLT:
                        WFT_exists = 1
                        WFT2FLT_path = shutil.copy("ProgramFiles/WFT2FLTN.EXE", path)  # Copy the WFT2FLT program into the given path.
                        WFT2FLT_command_path = WFT2FLT_path + " -dir=."  # This is the full command that is used in the cmd.

                        os.chdir(path)  # Run cmd through the given path.
                        os.system(WFT2FLT_command_path)  # Run the WFT2FLT program using cmd.
                        os.remove(WFT2FLT_path)  # Remove the WFT2FLT.EXE file from the path.

                        files = os.listdir(path)
                        os.makedirs(path + '/' + "Original WFT Files")
                        for file in files:
                            file_name, file_type = os.path.splitext(file)
                            file_type = file_type[1:]
                            if file_type == "WFT":
                                shutil.move(path + "/" + file, path + '/' + "Original WFT Files")

                    else:
                        WFT_exists = 0

                    os.chdir(path)  # Run cmd through the given path.

                    files = os.listdir(path)
                    num_of_experiments = int((len(files) - WFT_exists) / 2)

                    #   Check if there is already an existing report in the path folder.
                    #   if so, don't include it in the experiments count.
                    for file in files:
                        file_name, file_type = os.path.splitext(file)
                        file_type = file_type[1:]
                        if file_type == "html":
                            num_of_experiments -= 1

                    experiments = []
                    exp_num = 0

                    while True:
                        # This loop creates the new directories based on the file types and divides the files
                        # into their newly created directory. It also renames them accordingly (incid, trans).
                        file = files[0]
                        file_name, file_type = os.path.splitext(files[0])
                        file_type = file_type[1:]

                        if file_type != "":

                            exp_num += 1
                            os.makedirs(path + '/' + "Exp #" + str(exp_num))

                            #   Name of the folder the file should be moved into:
                            directory = path + '/' + "Exp #" + str(exp_num) + '/' + file_type

                            if not os.path.isdir(directory):
                                # create the folder if it doesn't exist:
                                os.makedirs(directory)

                            #   Move the experiment files to the folder:
                            shutil.move(path + '/' + files[0], path + '/' + "Exp #" + str(exp_num) + '/' + file_type)
                            old_path = path + '/' + "Exp #" + str(exp_num) + '/' + file_type + '/' + files[0]
                            new_path = path + '/' + "Exp #" + str(exp_num) + '/' + file_type + '/' + "incid." + file_type
                            os.rename(old_path, new_path)
                            experiments.append(["Exp #" + str(exp_num), new_path])

                            shutil.move(path + '/' + files[1], path + '/' + "Exp #" + str(exp_num) + '/' + file_type)
                            old_path = path + '/' + "Exp #" + str(exp_num) + '/' + file_type + '/' + files[1]
                            new_path = path + '/' + "Exp #" + str(exp_num) + '/' + file_type + '/' + "trans." + file_type
                            os.rename(old_path, new_path)
                            experiments.append(["Exp #" + str(exp_num), new_path])

                            files = os.listdir(path)

                        else:
                            #   if the current file is a folder, remove it from the files list.
                            files.remove(file)

                        #   Search for remaining experiment files.
                        #   If there are no remaining experiment files,
                        #   the process is complete and the 'While' loop can be exited.
                        found_exp_files = False
                        for file in files:
                            file_name, file_type = os.path.splitext(file)
                            exp_file_type = file_type[1:]

                            if file_type != "":
                                found_exp_files = True
                                break

                        if not found_exp_files:
                            break

                else:
                    # If there are already experiment directories, arranging has already been done.
                    # Thus, there are as many directories as experiments.

                    files = os.listdir(path + "/Exp #1")
                    for file in files:
                        #   The name of the folder inside the first experiment
                        #   will be the name of the file type that is used.
                        file_name, file_type = os.path.splitext(file)
                        file_type = file_type[1:]
                        if file_type == '':
                            exp_file_type = file_name
                            break

                    exp_count = 0
                    files = os.listdir(path)
                    for file in files:
                        file_name, file_type = os.path.splitext(file)
                        file_type = file_type[1:]
                        if "Exp" == file.split(" ")[0]:
                            exp_count += 1

                    num_of_experiments = exp_count

                    for file in files:
                        file_name, file_type = os.path.splitext(file)
                        file_type = file_type[1:]
                        if file_type == "html":
                            num_of_experiments -= 1

                return num_of_experiments, exp_file_type

            except Exception as exception:
                print(exception)


def set_path_input_thermal(path, two_bar_g_path):
    """
    Sets the path and converts WFT files to FLT if they exist.
    Since in Thermal Analysis the user manually chooses which file is which,
    no further file arranging is needed.
    """
    if path != "" and os.path.isdir(path):
        try:
            os.chdir(path)  # Run cmd through the given path.
            files = os.listdir(path)  # make a list of file names from the path directory

            '''
                The following loop will check if the data files are in WFT format.
                If so, a conversion to FLT file type will be made using the WFT2FLT.EXE program.   
            '''
            apply_WFT2FLT = False
            for file in files:
                file_name, file_type = os.path.splitext(file)
                file_type = file_type[1:]

                if file_type == "WFT":
                    apply_WFT2FLT = True
                    break

            if "Exp #1" not in files:
                # If there is at least one experiment folder then the WFT2FLT program has already been executed before,
                # and there is no need to run it again. This condition can save startup time.

                os.chdir(two_bar_g_path)  # Run cmd from this program's (main) path.

                if apply_WFT2FLT:
                    WFT_exists = 1
                    WFT2FLT_path = shutil.copy("ProgramFiles/WFT2FLTN.EXE", path)  # Copy the WFT2FLT program into the given path.
                    WFT2FLT_command_path = WFT2FLT_path + " -dir=."  # This is the full command that is used in the cmd.

                    os.chdir(path)  # Run cmd through the given path.
                    os.system(WFT2FLT_command_path)  # Run the WFT2FLT program using cmd.
                    os.remove(WFT2FLT_path)  # Remove the WFT2FLT.EXE file from the path.

                    files = os.listdir(path)
                    os.makedirs(path + '/' + "Original WFT Files")
                    for file in files:
                        file_name, file_type = os.path.splitext(file)
                        file_type = file_type[1:]
                        if file_type == "WFT":
                            shutil.move(path + "/" + file, path + '/' + "Original WFT Files")

                if file_type != "WFT":
                    file_type = file_type
                else:
                    file_type = "FLT"

            return 1, file_type

        except Exception as exception:
            print(exception)
    return 0, ""


def choose_path():
    """
    #   This functions uses easygui's directory chooser and sets the given path into the program.
    #   changes the path input to a new path given by user's input text
    #   opens the file browser
    """
    try:
        path = diropenbox()
        if path != "":

            os.chdir(path)  # Run cmd through the given path.
            files = os.listdir(path)  # make a list of file names from the path directory

            #   These are the only file types accepted by main
            valid_file_types = ["WFT", "FLT", "txt", "xlsx", "csv"]

            #   Search for files that are not acceptable:
            invalid_folder = False
            for file in files:

                #   Folder MUST be empty of irrelevant files for proper analysis of data.

                file_name, file_type = os.path.splitext(file)
                file_type = file_type[1:]

                if file_type not in valid_file_types:
                    invalid_folder = True

            if not invalid_folder or "Exp #1" in files:
                return path

            else:
                return None

        return None

    except Exception as exception:
        print(exception)