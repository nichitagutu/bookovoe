from constants import ROMANIAN_LETTERS


def remove_duplicates(items):
    return list(set(items))


def to_lower_case(word_list):
    return [word.lower() for word in word_list]


def filter_romanian_letters(word):
    return "".join([char for char in word if char in ROMANIAN_LETTERS])
