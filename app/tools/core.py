import typing as t
import numpy as np
import pandas as pd
import os

def read_file(path: str) -> pd.DataFrame:
    filename, file_extension = os.path.splitext(path)
    print(f'Core:: Get filename: {filename} and extension: {file_extension}')
    if file_extension in (".csv", ".txt"):
        df = pd.read_csv(path, sep=",", comment="#")
    elif file_extension in (".xls", ".xlsx"):
        df = pd.read_excel(path)
    else: 
        raise FileNotFoundError('Invalid file extension')
    return df
    
def save_file(path: str, df: pd.DataFrame):
    filename, file_extension = os.path.splitext(path)
    print(f'Core:: Get filename: {filename} and extension: {file_extension}')
    if file_extension in (".csv", ".txt"):
        df.to_csv(path)
    elif file_extension in (".xls", ".xlsx"):
        df.to_excel(path)
    else:
        raise FileNotFoundError('Invalid file extension') 

def convert_text_to_numeric_by_presence(word_list: t.List[str]):
    convert_map = {}
    current_class = 1
    numeric_list = []
    numbers = 0
    for value in word_list:
        if type(value) == int or type(value) == float:
            numbers += 1
        if value not in convert_map:
            convert_map[value] = current_class
            current_class += 1
        numeric_list.append(convert_map[value])
    if numbers == len(word_list):
        print(f'Core:: Current column is already numeric, no changes will be applied')
        return None
    return numeric_list


def convert_text_to_numeric_by_alphabet_order(word_list: t.List[str]):
    alph_word_list = np.copy(word_list)
    alph_word_list.sort()
    convert_map = create_map(alph_word_list)
    numeric_list = []
    numbers = 0
    for value in word_list:
        if type(value) == int or type(value) == float:
            numbers += 1
        numeric_list.append(convert_map[value])
    if numbers == len(word_list):
        print(f'Core:: Current column is already numeric, no changes will be applied')
        return None
    return numeric_list


def create_map(word_list: t.List[str]):
    index = 1
    convert_map = {}
    for word in word_list:
        if word not in convert_map:
            convert_map[word] = index
            index += 1
    return convert_map


def discretisation(values: t.List[str], divisions: int = 3):
    if not check_if_only_numeric(values):
        print(f'Core:: Only numeric values can be discretized')
        return None
    min_val = min(values)
    max_val = max(values)
    length = (max_val - min_val)/divisions
    bins = []
    for i in range(1, divisions):
        bins.append(min_val + i * length)
    return np.digitize(values, bins)


def standarization(values: t.List[str]):
    if not check_if_only_numeric(values):
        print(f'Core:: Only numeric values can be standarized')
        return None
    mean = np.mean(values)
    std = np.std(values)
    standarize_values = []
    for value in values:
        standarize_values.append(round((value-mean)/std, 2))
    return standarize_values


def change_data_range(values: t.List[str], min: int, max: int):
    old_min = np.min(values)
    old_max = np.max(values)
    old_range = (old_max - old_min)
    new_range = (max - min)
    new_values = []
    for value in values:
        new_values.append((((value - old_min) * new_range) / old_range) + min)
    return new_values

def check_if_only_numeric(values: t.List[str]):
    for value in values:
        if type(value) != int and type(value) != float:
            print(f'Not numeric value: {value}')
            return False
    return True