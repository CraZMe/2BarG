# 2BarG
 
 The Dynamic Fracture Laboratory, Faculty of Mechanical Engineering, Technion Israel Institue of Technology, 2022.
 
 Developed by Tzvi Gershanik, Itay Levin and Prof. Daniel Rittel.
 
2BarG is a program that analyses Split Hopkinson (Kolsky) Pressure Bar experiments. It is Python-based and features several libraries that make processing fast, simple, and efficient with minimal operator’s intervention. The program performs automatic identification of the incident, reflected and transmitted signals from the recorded experimental raw signals. The software reduces the data into stresses, strains, and velocities following the mandatory wave dispersion correction. A user-friendly and intuitive graphic interface allows for straightforward data reduction for various experimental specimens (standard or customized) and testing configurations (tension, compression, and shear). 

A paper on this program has been published through Elsevier's SoftwareX and is available in https://www.sciencedirect.com/science/article/pii/S2352711022000644 .

Furthermore, analysis of thermal effects is being developed and will be available in version 1.1. This, includes the usage of user inputted calibration files to create a mechanical - thermal viewpoint of the split Hopkinson pressure bar. 

**Versions:**
The first version's (1.0.0) code is available in my other repository - 2BarG_V1.
The current version (1.1.0) has been rearranged in a more modular architecture, which can be viewed schematically in the included Flow hart. 
 
 **Linux / Mac Users**
There exists a branch called Linux, which should can be used in linux distributions / mac OS. Note that this version is different than the main one (for windows) since it does not support WFT files (specifically - their conversion into FLT (txt) files done by the WFT2FLT.EXE program that can be found in the 2BarG Program Files folder).  

# General Info & Required Libraries
2BarG was developed in Python, using the Kivymd GUI. The following libraries **must** be installed for full operation of the software:

* Kivy
* Kivymd (0.104.2)
* Numpy
* Pandas
* SciPy
* Plotly
* Matplotlib
* csv
* easygui

We packaged 2BarG using PyInstaller, and a zipped file with an excecutable of the current version can be found at https://rittel.group/downloads/.

