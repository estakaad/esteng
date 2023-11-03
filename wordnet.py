import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

def find_homonym_pos(word):
    synsets = wn.synsets(word)

    pos_tags = set()

    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.name() == word:
                pos_tags.add(synset.pos())

    return list(pos_tags)


def get_definitions(word):
    # Find synsets for the given word
    synsets = wn.synsets(word)

    # Get definitions for each synset
    definitions = {synset: synset.definition() for synset in synsets}

    return definitions


#words = ["agape", "dupe", "dope", "ash", "confront"]
words = ["agape"]

for w in words:
    print(find_homonym_pos(w))
    print(get_definitions(w))