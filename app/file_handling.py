from os import path

from utilities import to_lower_case, remove_duplicates
from wordnet_interface import parse_synset_literal
from text_processing import (
    remove_non_letters,
    process_long_text,
    process_short_text,
)


def read_file_content(file_name):
    with open(path.join("text_samples", file_name), "r") as file:
        text = file.read()
        words = text.split()
        return to_lower_case(remove_non_letters(remove_duplicates(words)))


def write_synset_definitions_to_file(file_name, synset_ids, wordnet):
    with open(file_name, "a") as file:
        for synset_id in synset_ids:
            synset = wordnet.synset(synset_id)
            words = parse_synset_literal(wordnet, synset.literals)
            definition = synset.definition
            file.write(f"{words} ——— {definition}\n")


def get_lemmas_from_file(cube, words):
    words_string = " ".join(words)
    if len(words_string) > 512:
        return process_long_text(words)

    return process_short_text(cube, words_string)
