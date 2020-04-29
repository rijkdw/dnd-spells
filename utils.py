def remove_duplicates(list_arg):
    unique_list = []
    for item in list_arg:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list
