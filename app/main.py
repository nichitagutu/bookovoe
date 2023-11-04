from os import path
from itertools import chain

import rowordnet as rwn
from cube.api import Cube

from dotenv import load_dotenv

load_dotenv()

WORDNET = rwn.RoWordNet()

CUBE = Cube(verbose=True)
CUBE.load("ro")

ROMANIAN_LETTERS = "aăâbcdefghiîjklmnopqrsștțuvwxyz"


def get_lemmas_from_document(document):
    lemmas = []
    for sentence in document.sentences:
        for word in sentence.words:
            lemmas.append(word.lemma)

    return lemmas


def process_short_text(words_string):
    document = CUBE(words_string)
    return get_lemmas_from_document(document)


def chunk_words(words, max_length):
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_chunk) > max_length:
            yield " ".join(current_chunk)
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word)

    if current_chunk:
        yield " ".join(current_chunk)


def process_long_text(words):
    MAX_SEQUENCE_LENGTH = 512
    lemmas = []

    words_chunks = list(chunk_words(words, MAX_SEQUENCE_LENGTH))

    for chunk in words_chunks:
        lemmas.extend(process_short_text(chunk))

    return lemmas


def get_lemmas_from_file(words):
    words_string = " ".join(words)
    if len(words_string) > 512:
        return process_long_text(words)

    return process_short_text(words_string)


def read_file_content(file_name):
    with open(
        path.join(path.dirname(__file__), "text_samples", file_name), "r"
    ) as file:
        text = file.read()
        words = text.split()
        return to_lower_case(remove_non_letters(remove_duplicates(words)))


def parse_synset_literal(synset_literals):
    parsed_literals = [literal.replace("_", " ") for literal in synset_literals]
    return ", ".join(parsed_literals)


def remove_duplicates(items):
    return list(set(items))


def to_lower_case(word_list):
    return [word.lower() for word in word_list]


def filter_romanian_letters(word):
    return "".join([char for char in word if char in ROMANIAN_LETTERS])


def remove_non_letters(word_list):
    filtered_words = [filter_romanian_letters(word.lower()) for word in word_list]
    return [word for word in filtered_words if word]


def fetch_synset_ids_for_words(words):
    synsets = (WORDNET.synsets(literal=word, strict=True) for word in words)
    all_synsets = chain.from_iterable(synsets)
    return remove_duplicates(all_synsets)


def write_synset_definitions_to_file(file_name, synset_ids):
    with open(file_name, "a") as file:
        for synset_id in synset_ids:
            synset = WORDNET.synset(synset_id)
            words = parse_synset_literal(synset.literals)
            definition = synset.definition
            file.write(f"{words} ——— {definition}\n")


def main():
    input_file_name = input("Enter file name: ")
    words_from_file = read_file_content(input_file_name)
    lemmas = get_lemmas_from_file(words_from_file)
    synset_ids = fetch_synset_ids_for_words(lemmas)
    write_synset_definitions_to_file(
        input_file_name.replace(".txt", "_out.txt"), synset_ids
    )


def check_word_exists(word):
    word = word.lower()
    synset_ids = WORDNET.synsets(literal=word, strict=True)
    if synset_ids:
        for synset_id in synset_ids:
            synset = WORDNET.synset(synset_id)
            words = parse_synset_literal(synset.literals)
            definition = synset.definition
            print(f"{words} ——— {definition}")


if __name__ == "__main__":
    main()
