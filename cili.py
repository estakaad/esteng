import nltk
from nltk.corpus import wordnet as wn
from estnltk.wordnet import Wordnet

nltk.download('wordnet')

est_wn = Wordnet()

# Function to load ILI mappings from a file
def load_ili_mappings(file_path):
    mappings = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                mappings[parts[0]] = parts[1]
    return mappings


def find_keys_for_value(dictionary, target_value):
    return [key for key, value in dictionary.items() if value == target_value]


def synset_ids_and_ilis():
    est_ili_file = 'wordnettest/est_ili.txt'
    eng_ili_file = 'wordnettest/eng_ili.txt'

    est_ili_mappings = load_ili_mappings(est_ili_file)
    eng_ili_mappings = load_ili_mappings(eng_ili_file)

    # Words to be compared
    estonian_word = "vähk"
    english_word = "cancer"

    # Synsets of the words
    estonian_word_synsets = est_wn[estonian_word]
    english_word_synsets = wn.synsets(english_word)

    est_synset_ids = []
    eng_synset_ids = []

    est_ilis = []
    eng_ilis = []

    est_defs = []
    eng_defs = []

    # Synset IDS
    for est in estonian_word_synsets:
        est_wn_id = est.estwn_id.replace('estwn-et-', '')
        est_synset_ids.append(est_wn_id)
        est_ilis.append(est_ili_mappings.get(est_wn_id))
        est_defs.append(est.definition)

    for eng in english_word_synsets:
        eng_wn_id = f"{str(eng.offset()).zfill(8)}-{eng.pos()}"
        eng_synset_ids.append(eng_wn_id)
        eng_ilis.append(eng_ili_mappings.get(eng_wn_id))
        eng_defs.append(eng.definition())


    print(est_synset_ids)
    print(est_defs)
    print(est_ilis)
    print('')
    print(eng_synset_ids)
    print(eng_defs)
    print(eng_ilis)

    return est_ilis, eng_ilis


def print_lemmas_of_synsets(eng_ili_file):
    eng_ili_mappings = load_ili_mappings(eng_ili_file)

    for synset_id in eng_ili_mappings.keys():
        # Extract the offset and pos from synset_id
        offset, pos = synset_id.split('-')
        offset = int(offset)

        # Find the synset in NLTK WordNet
        synset = wn.synset_from_pos_and_offset(pos, offset)

        # Print synset ID and ILI
        print(f"Synset ID: {synset_id}, ILI: {eng_ili_mappings[synset_id]}")

        # Get lemmas of the synset
        lemmas = synset.lemmas()

        if lemmas:
            lemma_names = [lemma.name() for lemma in lemmas]
            print("Lemmas:", ", ".join(lemma_names))
        else:
            print("No lemmas found for this synset.")

        print()

def has_common_element(list1, list2):
    return bool(set(list1) & set(list2))

est_ilis, eng_ilis = synset_ids_and_ilis()

print(has_common_element(est_ilis, eng_ilis))