from itertools import chain
from utilities import remove_duplicates


def parse_synset_literal(synset_literals):
    parsed_literals = [literal.replace("_", " ") for literal in synset_literals]
    return ", ".join(parsed_literals)


def fetch_synset_ids_for_words(wordnet, words):
    synsets = (wordnet.synsets(literal=word, strict=True) for word in words)
    all_synsets = chain.from_iterable(synsets)
    return remove_duplicates(all_synsets)
