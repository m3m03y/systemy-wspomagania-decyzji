import pandas as pd
import PySimpleGUI as sg
import numpy as np
import os
import tools.core as core
from table import create_table
working_directory = os.getcwd()

layout = [
    [sg.Text("Choose file:")],
    [sg.InputText(key="-FILE_PATH-"),
     sg.FileBrowse(initial_folder=working_directory)],
    [sg.Button("Submit"), sg.Exit()]
]

window = sg.Window("Display CSV", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == "Submit":
        excel_file_path = values["-FILE_PATH-"]
        try:
            excel_file_df = core.read_file(excel_file_path)
        except:
            print("File read error") 
        headers = excel_file_df.columns.to_numpy()
        data_array = excel_file_df.to_numpy()
        # ndarray
        create_table(headers.tolist(), data_array.tolist())
window.close()
