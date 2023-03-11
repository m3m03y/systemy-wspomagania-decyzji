import typing as t

from numpy import copy

def convert_text_to_numeric_by_presence(word_list: t.List[str]):
    convert_map = {}
    current_class = 1
    numeric_list = []
    for value in word_list:
        if value not in convert_map:
            convert_map[value] = current_class
            current_class+=1
        numeric_list.append(convert_map[value]) 
    return numeric_list

def convert_text_to_numeric_by_alphabet_order(word_list: t.List[str]):
    alph_word_list = copy(word_list)
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
            index+=1
    return convert_map