import datetime
import time
import functools

school_dict = {
    'A': 'Abjuration', 'C': 'Conjuration', 'D': 'Divination', 'V': 'Evocation',
    'E': 'Enchantment', 'I': 'Illusion', 'N': 'Necromancy', 'T': 'Transmutation'
}

rev_school_dict = {}
for (key, val) in zip(list(school_dict.keys()), list(school_dict.values())):
    rev_school_dict[val] = key


school_list = list(school_dict.values())


def get_time(output_format='%H:%M:%S'):
    return datetime.datetime.now().strftime(output_format)


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        # print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def remove_duplicates(list_arg):
    unique_list = []
    for item in list_arg:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def remove_empty_strings(list_arg):
    non_empty_list = []
    for item in non_empty_list:
        if len(item) > 0:
            non_empty_list.append(item)
    return non_empty_list


def title_case(sentence):
    non_upper_words = ['the', 'a', 'of']
    new_words = [sentence.split(' ')[0].capitalize()]
    if len(sentence.split(' ')) > 1:
        for word in sentence.split(' ')[1:]:
            if word not in non_upper_words:
                new_words.append(word.capitalize())
    return ' '.join(new_words)
