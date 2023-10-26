from bs4 import BeautifulSoup, Tag, NavigableString
import re
import json
from collections import defaultdict


html_file_path = 'failid/sõnastikud/keelevara/et-en_silvet/HTML.html'

with open(html_file_path, 'r', encoding='utf-8') as f:
    html_data = f.read()

soup = BeautifulSoup(html_data, 'html.parser')

roman_numeral_pattern = re.compile(r'<big><b>(I|II|III|IV|V|VI|VII)</b></big>')
empty_brackets_pattern = re.compile(r'\[\s*\]\s*')

extracted_content = []

for element in soup.find_all(class_='mrks'):
    content_list = []
    term = element.get_text()

    sibling = element.next_sibling
    while sibling:
        if isinstance(sibling, Tag):
            if sibling.has_attr('class') and 'mrks' in sibling['class']:
                break
            content_list.append(str(sibling).strip())
        elif isinstance(sibling, NavigableString):
            content_list.append(str(sibling).strip())

        sibling = sibling.next_sibling if sibling else None

    content_between_mrks = ' '.join(content_list).replace('\n', ' ').replace('&nbsp;', ' ')

    soup_content = BeautifulSoup(content_between_mrks, 'html.parser')

    if roman_numeral_pattern.search(content_between_mrks):
        for tag_type in ['term', 'stiil']:
            for tag in soup_content.find_all('i', {'class': tag_type}):
                tag.decompose()
        for tag_type in ['ipa']:
            for tag in soup_content.find_all('span', {'class': tag_type}):
                tag.decompose()

        content_between_mrks = str(soup_content).strip()

        content_between_mrks = roman_numeral_pattern.sub('', content_between_mrks)
        content_between_mrks = empty_brackets_pattern.sub('', content_between_mrks)
        extracted_content.append([term, content_between_mrks.strip()])


json_output = {}

for term, definition in extracted_content:
    if term not in json_output:
        json_output[term] = []
    json_output[term].append(definition)

for headword, definitions in json_output.items():
    new_definitions_grouped = defaultdict(list)
    for definition in definitions:
        soup = BeautifulSoup(definition, 'html.parser')

        pos_tag = soup.find('i', {'class': 'sl'})
        pos_tag = soup.find('i', {'class': 'sl'})
        if pos_tag:
            if pos_tag.text.startswith('v'):
                new_pos = 'v'
            else:
                new_pos = pos_tag.text
        else:
            new_pos = "unknown"

        for tag in soup.find_all('b', {'class': 'nr'}):
            tag.decompose()
        if pos_tag:
            pos_tag.decompose()

        cleaned_definition = str(soup).strip()

        if '<b class=\"nr\">' in definition:
            split_definitions = [x for x in re.split(r'(<b class=\"nr\">[0-9]+<\/b>)', definition) if x.strip()]

            combined_definitions = ["".join(split_definitions[i:i + 2]) for i in range(1, len(split_definitions), 2)]

            new_definitions_grouped[new_pos].extend(combined_definitions)
        else:
            new_definitions_grouped[new_pos].append(cleaned_definition)

    json_output[headword] = dict(new_definitions_grouped)

new_json_output = {}
for headword, pos_dict in json_output.items():
    new_pos_dict = defaultdict(list)
    for pos, definitions in pos_dict.items():
        for definition in definitions:
            soup = BeautifulSoup(definition, 'html.parser')

            pos_tag = soup.find('i', {'class': 'sl'})
            if pos_tag:
                if pos_tag.text.startswith('v'):
                    new_pos = 'v'
                else:
                    new_pos = pos_tag.text
            else:
                new_pos = "unknown"

            cleaned_definition = re.sub(r'<b class=\"nr\">[0-9]+<\/b>', '', definition)
            cleaned_definition = re.sub(r'<\/?b>', '', cleaned_definition)
            cleaned_definition = re.sub(r'<i class=\"sl\">.*<\/i>', '', cleaned_definition)
            cleaned_definition = cleaned_definition.replace('<br/>', '')
            cleaned_definition = cleaned_definition.replace('\xad', '')
            cleaned_definition = cleaned_definition.replace('<i>', '')
            cleaned_definition = cleaned_definition.replace('</i>', '')
            cleaned_definition = re.sub('<mid>.*$', '', cleaned_definition)
            new_pos_dict[new_pos].append(cleaned_definition.strip().strip(';'))

    new_json_output[headword] = dict(new_pos_dict)

with open('output/homonyms_silvet.json', 'w', encoding='utf-8') as f:
    json.dump(new_json_output, f, ensure_ascii=False, indent=4)