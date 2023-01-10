# %%
# Imports
import numpy as np
import pandas as pd
import csv 
import sys
import time
import os
import shutil
import PySimpleGUI as sg

# %%
# Timestamp 

timestr = time.strftime("%Y%m%d-%H%M%S")


# %%
# Inputs
input_file_folder = "/Users/keltoumboukra/Desktop/Coding projects - Git/SamplePoolingForNGS/Files/ClariostarOutputs/"
input_file_name = "qubit_data_Marko_22112022.CSV"

# final desired vol (nL)
final_pool_vol = 10000

# well position of pool in output plate
pool_well_in_output_plate = "B1"

# minimum volume to be pipetted (nL)
min_pipetting_capacity = float(25) # for Echo

# minimum volume that can be pipetted 
vol_available_in_well = 10000 # for e.g, if there is 20 uL in the well, 5000 nL is what can be available as 15 uL is the minimum working range in the PP-0200 Echo plate)

# Beckman or Echo
BeckmanOrEcho = "Echo"


# %%
# Ask user which platform to use: Beckman or Echo

sg.theme('LightBrown9')
    
layout = [
        [sg.Text('Choose automated platform to use:\n\t- Echo: non genomic DNA\n\t- Beckman: genomic DNA')],
        [sg.Text('Desired platform name ("Echo" or "Beckman"):')],
        [sg.InputText("Echo")],
        [sg.Submit(), sg.Cancel()]
        ]

window = sg.Window('NGS Pooling', layout)
event, values = window.read()
window.maximize()
window.close()

BeckmanOrEcho = values[0]


# %%
# Create GUI

sg.theme('LightBrown9')


if BeckmanOrEcho == "Echo":
    layout = [
        [sg.Text('Please enter the desired parameters')],
        [sg.Text('Input file folder (ending with /)', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Desktop/Coding projects - Git/SamplePoolingForNGS/Files/ClariostarOutputs/")],
        [sg.Text('Input file name', size =(25, 1)), sg.InputText("qubit_data_Marko_22112022.CSV")],
        [sg.Text('Output file folder (ending with /)', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Desktop/Coding projects - Git/SamplePoolingForNGS/Files/")],
        [sg.Text('Final pool volume (nL)', size =(25, 1)), sg.InputText("1000")],
        [sg.Text('Pooling well position', size =(25, 1)), sg.InputText("B1")],
        [sg.Text('Minimum pipetting capacity (nL)', size =(25, 1)), sg.InputText("25")],
        [sg.Text('Sample volume available (nL)', size =(25, 1)), sg.InputText("5000")],
        [sg.Submit(), sg.Cancel()]
    ]

elif BeckmanOrEcho == "Beckman":
    layout = [
        [sg.Text('Please enter the desired parameters')],
        [sg.Text('Input file folder (ending with /)', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Desktop/Coding projects - Git/SamplePoolingForNGS/Files/ClariostarOutputs/")],
        [sg.Text('Input file name', size =(25, 1)), sg.InputText("qubit_data_Marko_22112022.CSV")],
        [sg.Text('Output file folder (ending with /)', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Desktop/Coding projects - Git/SamplePoolingForNGS/Files/")],
        [sg.Text('Final pool volume (uL)', size =(25, 1)), sg.InputText("10")],
        [sg.Text('Pooling well position', size =(25, 1)), sg.InputText("B1")],
        [sg.Text('Minimum pipetting capacity (uL)', size =(25, 1)), sg.InputText("0.5")],
        [sg.Text('Sample volume available (uL)', size =(25, 1)), sg.InputText("25")],
        [sg.Submit(), sg.Cancel()]
    ]

window = sg.Window('Robot File Generator For NGS Pooling', layout)
event, values = window.read()
window.maximize()
window.close()    

# Assigning values 
input_file_folder = values[0]
input_file_name = values[1]
output_files_folder = values[2]
final_pool_vol = float(values[3])
pool_well_in_output_plate = values[4]
min_pipetting_capacity = float(values[5])
vol_available_in_well = float(values[6])

# Dataframes
input_file_df = pd.read_csv(input_file_folder + input_file_name)
input_file_df.rename(columns={input_file_df.columns[2]: "Concentration"},inplace=True)


# %%
# Outputs

output_files_folder = output_files_folder + "NGSpooling_" + timestr
os.mkdir(output_files_folder)
output_files_folder = output_files_folder + "/"

output_file_name = "ProcessingDetails.csv"
output_file_df = pd.DataFrame(columns=['Sample Well ID','Sample Concentration','Sample Calculated Weight', 'Sample Calculated Weight Normalised', 'Sample Calculated Volume In Pool'])

if BeckmanOrEcho == "Echo":
    output_echo_file_name = "EchoFile.csv"
    output_echo_file_df = pd.DataFrame(columns=['Source Well','Destination Well','Transfer Volume'])
elif BeckmanOrEcho == "Beckman":
    output_beckman_file_name = "BeckmanFile.csv"
    output_beckman_file_df = pd.DataFrame(columns=['Source Well','Destination Well','Transfer Volume'])    

output_report_name = "ExceptionsReport.csv"
output_report_df = pd.DataFrame(columns=['Sample Well ID','Sample Concentration','Comment'])

# Copy input file into the output folder
os.mkdir(output_files_folder + "InputFiles/")
shutil.copyfile(input_file_folder+input_file_name, output_files_folder + "InputFiles/" + "InputFile.csv")


# %%
# Trim input data frame 

# Remove standards 
input_file_df = input_file_df[input_file_df["Content"].str.contains("Standard") == False]
input_file_df = input_file_df.reset_index(drop=True)

# Remove samples with negative concentrations and add to output report
for row in input_file_df.itertuples():
    
    Index = row [0]
    Well = row[1]
    Concentration = row[3]
    
    if Concentration <= 0:
        output_report_df = output_report_df.append({'Sample Well ID': Well, 'Sample Concentration': Concentration, 'Comment': "Sample has negative value for concentration"}, ignore_index=True)
        input_file_df = input_file_df.drop(Index)

input_file_df = input_file_df.reset_index(drop=True)
output_report_df = output_report_df.reset_index(drop=True)

# Copy trimmed input file into the output folder
input_file_df.to_csv(output_files_folder + "InputFiles/" + "InputTrimmedFile.csv", index=False)

# %%
# Calculate Weights 

max_concentration = input_file_df['Concentration'].max()
sum_weights = float()

for row in input_file_df.itertuples():
    
    Index = row [0]
    Well = row[1]
    Concentration = row[3]

    sample_weight = max_concentration/Concentration
    sum_weights += sample_weight
    output_file_df = output_file_df.append({'Sample Well ID': Well, 'Sample Concentration': Concentration, 'Sample Calculated Weight': sample_weight}, ignore_index=True)  
    

# %%
# Calculate Normalised Weights 

sum_normalised_weights = float(0)
for row in input_file_df.itertuples():
    
    Index = row [0]
    Well = row[1]
    Concentration = row[3]
    
    sample_normalised_weight = output_file_df["Sample Calculated Weight"].iloc[Index]/sum_weights
    sum_normalised_weights += sample_normalised_weight # for QC, should be =1
    output_file_df.at[Index,'Sample Calculated Weight Normalised']=sample_normalised_weight

# %%
# Calculate Volume to pipette for each sample in the final pool

vol_in_pool = float()
sum_vol_in_pool = float(0)
fail_bool = bool(0)

for row in input_file_df.itertuples():
    
    Index = row [0]
    Well = row[1]
    Concentration = row[3]
    
    vol_in_pool = output_file_df["Sample Calculated Weight Normalised"].iloc[Index]*final_pool_vol 
    sum_vol_in_pool += vol_in_pool # for QC, should be = final_pool_vol  
    
    if vol_in_pool < min_pipetting_capacity:
        output_report_df = output_report_df.append({'Sample Well ID': Well, 'Sample Concentration': Concentration, 'Comment': "Volume to be pipetted for this well ({} nL) is smaller than pipetting capacity ({} nL). You MUST reprocess the file".format(vol_in_pool,min_pipetting_capacity)}, ignore_index=True)
        fail_bool = bool(1)
    elif vol_in_pool > vol_available_in_well:
        output_report_df = output_report_df.append({'Sample Well ID': Well, 'Sample Concentration': Concentration, 'Comment': "Volume to be pipetted for this well ({} nL) is larger than the volume available ({} nL). You MUST reprocess the file".format(vol_in_pool,vol_available_in_well)}, ignore_index=True)
        fail_bool = bool(1)
    else:
        output_file_df.at[Index,'Sample Calculated Volume In Pool']=vol_in_pool
        if BeckmanOrEcho == "Echo":
            output_echo_file_df = output_echo_file_df.append({'Source Well': Well, 'Destination Well': pool_well_in_output_plate, 'Transfer Volume': vol_in_pool}, ignore_index=True)
        elif BeckmanOrEcho == "Beckman":
            output_beckman_file_df = output_beckman_file_df.append({'Source Well': Well, 'Destination Well': pool_well_in_output_plate, 'Transfer Volume': vol_in_pool}, ignore_index=True)


# %%
# Calculate final pool concentration for QC 

sum_concentrations = float(0)

for row in output_file_df.itertuples():
    
    Concentration = row[2]
    VolInPool = row[5]
    
    sum_concentrations += (Concentration*VolInPool)

final_pool_concentration = "%.3f"%(sum_concentrations / final_pool_vol)

# %%
# Export files and communicate outcome to user in GUI

os.mkdir(output_files_folder + "OutputFiles/")

if BeckmanOrEcho == "Echo":
    if fail_bool == bool(1):
        layout = [[sg.Text("Processing failed. The concentration of 1 sample or more is out of range and doesn't allow pooling with the settings entered. Check report file for details.")], [sg.Button("OK")]]
        window = sg.Window("Echo File Generator For NGS Pooling", layout)
    else:
        output_file_df.to_csv(output_files_folder + "OutputFiles/" + output_file_name, index=False)
        output_echo_file_df.to_csv(output_files_folder + "OutputFiles/" + output_echo_file_name, index=False)
        layout = [[sg.Text("Processing successful! Final pool concentration: {} ng/uL.".format(final_pool_concentration))], [sg.Button("OK")]]
        window = sg.Window("Echo File Generator For NGS Pooling", layout)

elif BeckmanOrEcho == "Beckman":
    if fail_bool == bool(1):
        layout = [[sg.Text("Processing failed. The concentration of 1 sample or more is out of range and doesn't allow pooling with the settings entered. Check report file for details.")], [sg.Button("OK")]]
        window = sg.Window("Beckman File Generator For NGS Pooling", layout)
    else:
        output_file_df.to_csv(output_files_folder + "OutputFiles/" + output_file_name, index=False)
        output_beckman_file_df = output_beckman_file_df.sort_values(by='Transfer Volume', ascending=False)
        output_beckman_file_df.to_csv(output_files_folder + "OutputFiles/" + output_beckman_file_name, index=False)
        layout = [[sg.Text("Processing successful! Final pool concentration: {} ng/uL.".format(final_pool_concentration))], [sg.Button("OK")]]
        window = sg.Window("Beckman File Generator For NGS Pooling", layout)
    

output_report_df.to_csv(output_files_folder + "OutputFiles/" + output_report_name, index=False)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break
window.close()


# %%



