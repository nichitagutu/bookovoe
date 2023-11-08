from typing import List

from utilities import remove_duplicates

from constants import ROMANIAN_LETTERS


def get_lemmas_from_document(document):
    lemmas = []
    for sentence in document.sentences:
        for word in sentence.words:
            lemmas.append(word.lemma)

    return lemmas


def process_short_text(cube, words_string):
    document = cube(words_string)
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


def process_long_text(cube, words):
    MAX_SEQUENCE_LENGTH = 512
    lemmas = []

    words_chunks = list(chunk_words(words, MAX_SEQUENCE_LENGTH))

    for chunk in words_chunks:
        lemmas.extend(process_short_text(cube, chunk))

    return lemmas


def filter_romanian_letters(word: str) -> str:
    return "".join([char for char in word if char in ROMANIAN_LETTERS])


def remove_non_letters(word_list: List[str]) -> List[str]:
    filtered_words = [filter_romanian_letters(word.lower()) for word in word_list]
    return [word for word in filtered_words if word]


def to_lower_case(word_list: List[str]) -> List[str]:
    return [word.lower() for word in word_list]


def remove_underscores(synset_literals: List[str]) -> List[str]:
    return [literal.replace("_", " ") for literal in synset_literals]

def prepare_text(text: str) -> List[str]:
    words = text.split()
    return to_lower_case(remove_non_letters(remove_duplicates(words)))
