from bs4 import BeautifulSoup
import re


html_file_path = 'failid/sõnastikud/keelevara/et-en_silvet/HTML.html'

with open(html_file_path, 'r', encoding='utf-8') as f:
    html_data = f.read()

soup = BeautifulSoup(html_data, 'html.parser')

roman_numeral_pattern = re.compile(r'<big><b>(I|II|III|IV|V|VI|VII)</b></big>')

elements_with_mrks = soup.find_all(class_='mrks')

filtered_elements = []

for element in elements_with_mrks:
    next_sibling = element.find_next_sibling()

    content_between_mrks = str(element)

    while next_sibling and not next_sibling.has_attr('class'):
        content_between_mrks += str(next_sibling)
        next_sibling = next_sibling.find_next_sibling()

    if roman_numeral_pattern.search(content_between_mrks):
        filtered_elements.append(element)

for element in filtered_elements:
    print(element)