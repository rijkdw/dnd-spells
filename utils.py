school_dict = {
    'A': 'Abjuration', 'C': 'Conjuration', 'D': 'Divination', 'V': 'Evocation',
    'E': 'Enchantment', 'I': 'Illusion', 'N': 'Necromancy', 'T': 'Transmutation'
}

rev_school_dict = {}
for (key, val) in zip(list(school_dict.keys()), list(school_dict.values())):
    rev_school_dict[val] = key


school_list = list(school_dict.values())


def remove_duplicates(list_arg):
    unique_list = []
    for item in list_arg:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def title_case(sentence):
    non_upper_words = ['the', 'a', 'of']
    new_words = [sentence.split(' ')[0].capitalize()]
    if len(sentence.split(' ')) > 1:
        for word in sentence.split(' ')[1:]:
            if word not in non_upper_words:
                new_words.append(word.capitalize())
    return ' '.join(new_words)
