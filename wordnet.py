import json
import nltk
from nltk.corpus import wordnet as wn

# Ensure that WordNet is downloaded
nltk.download('wordnet')

# Mapping from WordNet POS codes to desired output POS codes
pos_mapping = {
    'n': 's',
    'v': 'v',
    'a': 'adj',
    's': 'adj',
    'r': 'adv'
}

def get_wordnet_definitions(word):
    """Retrieve definitions from WordNet for a given word."""
    synsets = wn.synsets(word)
    definitions_by_pos = {}
    for synset in synsets:
        pos = synset.pos()
        if pos not in definitions_by_pos:
            definitions_by_pos[pos] = []
        definitions_by_pos[pos].append(synset.definition())
    return definitions_by_pos

def process_data(data):
    """Process each entry in the data to enhance it with WordNet definitions."""
    for entry in data:
        syn_candidate_words = entry.get('synCandidateWords', [])
        new_syn_candidate_words = []

        for syn_word in syn_candidate_words:
            word_value = syn_word.get('value')
            existing_pos_codes = syn_word.get('posCodes', [])
            wordnet_definitions_by_pos = get_wordnet_definitions(word_value)

            # Process WordNet definitions
            for pos, definitions in wordnet_definitions_by_pos.items():
                mapped_pos = pos_mapping.get(pos, pos)

                # Check if this POS is already in existing POS codes
                if mapped_pos not in existing_pos_codes:
                    # Create a new entry for this POS
                    new_word_entry = {
                        "value": word_value,
                        "lang": "eng",
                        "weight": syn_word.get('weight', 1.0),
                        "posCodes": [mapped_pos],
                        "definitions": syn_word.get('definitions', []) + [{"value": defn, "sourceLinks": [{"sourceId": 84967, "value": "NLTK"}]} for defn in definitions],
                        "usages": syn_word.get('usages', [])
                    }
                    new_syn_candidate_words.append(new_word_entry)
                else:
                    # Append definitions to existing entry
                    for existing_word in new_syn_candidate_words:
                        if existing_word['value'] == word_value and mapped_pos in existing_word['posCodes']:
                            existing_word['definitions'].extend([{"value": defn, "sourceLinks": [{"sourceId": 84967, "value": "NLTK"}]} for defn in definitions])

            # Add the original word if it doesn't have any WordNet definitions
            if word_value and not wordnet_definitions_by_pos:
                new_syn_candidate_words.append(syn_word)

        # Replace the original list with the new one
        entry['synCandidateWords'] = new_syn_candidate_words

    return data

# Load the data from 'test.json'
with open('wordnettest/test.json', 'r') as file:
    data = json.load(file)

# Process the data
processed_data = process_data(data)

# Save the processed data to a new file
with open('wordnettest/enhanced_test.json', 'w') as file:
    json.dump(processed_data, file, indent=4)

print("Data processing complete. The enhanced data is saved in 'enhanced_test.json'.")
