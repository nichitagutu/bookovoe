from os import path
from typing import List

from wordnet_interface import get_synset_key_value_definitions
from utilities import remove_duplicates
from text_processing import (
    remove_non_letters,
    process_long_text,
    process_short_text,
    to_lower_case,
)


def read_file_content(file_name: str) -> List[str]:
    with open(path.join("text_samples", file_name), "r") as file:
        text = file.read()
        words = text.split()
        return to_lower_case(remove_non_letters(remove_duplicates(words)))


def write_synset_definitions_to_file(wordnet, synset_ids, file_name) -> None:
    with open(file_name, "a") as file:
        definitions = get_synset_key_value_definitions(wordnet, synset_ids)
        for key, value in definitions.items():
            file.write(f"{key}: {value}\n")


def get_lemmas_from_file(cube, words) -> List[str]:
    words_string = " ".join(words)
    if len(words_string) > 512:
        return process_long_text(words)

    return process_short_text(cube, words_string)
