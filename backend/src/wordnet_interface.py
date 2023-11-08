from typing import List, Dict
from itertools import chain

from utilities import remove_duplicates
from text_processing import remove_underscores
from rowordnet import RoWordNet


def fetch_synset_ids_for_lemmas(wordnet: RoWordNet, lemmas: List[str]) -> List[str]:
    synsets = (wordnet.synsets(literal=word, strict=True) for word in lemmas)
    all_synsets = chain.from_iterable(synsets)
    return remove_duplicates(all_synsets)


def get_synset_key_value_definitions(
    wordnet: RoWordNet, synset_ids: List[str]
) -> Dict[str, List[str]]:
    definitions: Dict[str, List[str]] = {}
    for synset_id in synset_ids:
        synset = wordnet.synset(synset_id)
        print("synset: ", synset)
        words = remove_underscores(synset.literals)
        definition = synset.definition
        for word in words:
            if word in definitions:
                definitions[word].append(definition)
                definitions[word] = list(set(definitions[word]))
            else:
                definitions[word] = [definition]

    return definitions
