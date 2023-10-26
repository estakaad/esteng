import json
import os
from collections import defaultdict, Counter
from lxml import etree

path = "failid/sõnastikud/kdict"
en_headword_counter = Counter()
en_headword_details = defaultdict(list)

for filename in os.listdir(path):
    if filename.endswith(".xml"):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            content = f.read()

        root = etree.fromstring(content)

        for entry in root.xpath('//DictionaryEntry'):
            en_headword = entry.xpath('.//EnHeadword/text()')
            en_pos = entry.xpath('.//EnPOS/text()')
            definition = entry.xpath('.//Definition/text()')

            if en_headword and en_pos and definition:
                en_headword = en_headword[0]
                en_pos = en_pos[0]
                definition = definition[0]

                en_headword_counter.update([en_headword])
                en_headword_details[en_headword].append({'POS': en_pos, 'Definition': definition.strip('.')})

homonyms_with_details = {}

for word, count in en_headword_counter.items():
    if count > 1:
        details = en_headword_details[word]
        unique_details = {}

        for d in details:
            pos = d['POS']
            definition = d['Definition']

            if pos not in unique_details:
                unique_details[pos] = []

            if definition not in unique_details[pos]:
                unique_details[pos].append(definition)

        is_homonym = len(unique_details) > 1 or any(len(defs) > 1 for defs in unique_details.values())

        if is_homonym:
            homonyms_with_details[word] = unique_details


sorted_homonyms_with_details = {k: homonyms_with_details[k] for k in sorted(homonyms_with_details)}

transformed_homonyms_with_details = {}

for word, details in sorted_homonyms_with_details.items():
    transformed_details = {}
    for pos, definitions in details.items():
        transformed_details[pos] = definitions
    transformed_homonyms_with_details[word] = transformed_details

with open('output/homonyms_kdict.json', 'w', encoding='utf-8') as f:
    json.dump(transformed_homonyms_with_details, f, ensure_ascii=False, indent=4)
