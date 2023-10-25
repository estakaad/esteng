from bs4 import BeautifulSoup, Tag, NavigableString
import re

# Your HTML file path
html_file_path = 'failid/sõnastikud/keelevara/et-en_silvet/HTML.html'

with open(html_file_path, 'r', encoding='utf-8') as f:
    html_data = f.read()

soup = BeautifulSoup(html_data, 'html.parser')

# Regex pattern to match Roman numerals
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
        for tag_type in ['sl', 'term', 'stiil']:
            for tag in soup_content.find_all('i', {'class': tag_type}):
                tag.decompose()
        for tag_type in ['ipa']:
            for tag in soup_content.find_all('span', {'class': tag_type}):
                tag.decompose()

        content_between_mrks = str(soup_content).strip()

        content_between_mrks = roman_numeral_pattern.sub('', content_between_mrks)
        content_between_mrks = empty_brackets_pattern.sub('', content_between_mrks)
        extracted_content.append([term, content_between_mrks.strip()])

output_file_path = 'output/homonyms_silvet.txt'

# Open the file and write the extracted content
with open(output_file_path, 'w', encoding='utf-8') as f:
    for content in extracted_content:
        f.write(str(content) + '\n')
