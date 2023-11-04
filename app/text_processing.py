from utilities import filter_romanian_letters


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


def remove_non_letters(word_list):
    filtered_words = [filter_romanian_letters(word.lower()) for word in word_list]
    return [word for word in filtered_words if word]
