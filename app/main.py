import rowordnet as rwn
from cube.api import Cube

from wordnet_interface import fetch_synset_ids_for_words
from file_handling import (
    read_file_content,
    get_lemmas_from_file,
    write_synset_definitions_to_file,
)

from dotenv import load_dotenv

load_dotenv()

WORDNET = rwn.RoWordNet()

CUBE = Cube(verbose=True)
CUBE.load("ro")


def main():
    input_file_name = input("Enter file name: ")
    words_from_file = read_file_content(input_file_name)
    lemmas = get_lemmas_from_file(CUBE, words_from_file)
    synset_ids = fetch_synset_ids_for_words(lemmas)
    write_synset_definitions_to_file(
        input_file_name.replace(".txt", "_out.txt"), synset_ids, WORDNET
    )


if __name__ == "__main__":
    main()
