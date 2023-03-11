import typing as t

def convert_text_to_numeric(word_list: t.List[str]):
    convert_map = {}
    current_class = 1
    numeric_list = []
    for value in word_list:
        if value not in convert_map:
            convert_map[value] = current_class
            current_class+=1
        numeric_list.append(convert_map[value]) 
    return numeric_list