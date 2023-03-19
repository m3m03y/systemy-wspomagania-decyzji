import typing as t
import numpy as np


def convert_text_to_numeric_by_presence(word_list: t.List[str]):
    convert_map = {}
    current_class = 1
    numeric_list = []
    for value in word_list:
        if value not in convert_map:
            convert_map[value] = current_class
            current_class += 1
        numeric_list.append(convert_map[value])
    return numeric_list


def convert_text_to_numeric_by_alphabet_order(word_list: t.List[str]):
    alph_word_list = np.copy(word_list)
    alph_word_list.sort()
    convert_map = create_map(alph_word_list)
    numeric_list = []
    for value in word_list:
        numeric_list.append(convert_map[value])
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
    min_val = min(values)
    max_val = max(values)
    length = (max_val - min_val)/divisions
    bins = []
    for i in range(1, divisions):
        bins.append(min_val + i * length)
    return np.digitize(values, bins)


def standarization(values: t.List[str]):
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
