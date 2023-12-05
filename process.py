from collections import Counter
import csv
from time import sleep

from bs4 import BeautifulSoup
import requests


stop_words = [
    "le", "la", "les", "de", "du", "des", "un", "une", "deux", "trois",
    "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "et", "ou",
    "car", "avec", "pour", "dans", "sur", "sous", "par", "entre", "vers",
    "ainsi", "mais", "donc", "or", "ni", "si", "que", "qui", "quoi", "où",
    "quand", "comment", "en", "ça", "ce", "ces", "ceux", "cette", "cet", "mon", "ton", "son", "mes", "tes", "ses"
]

phrase = "Le chat chat est sur le tapis"


# Functions - Étape 1
def text_to_words(text: str):
    array_of_words = text.lower().split()
    sorted_word_count = dict(sorted(Counter(array_of_words).items(), key=lambda x: x[1], reverse=True))
    return sorted_word_count


# Étape 2
def remove_stop_words(word_dict: dict, stop_words: list):
    for word in stop_words:
        if word in word_dict:
            del word_dict[word]
    return word_dict


# Étape 3
def get_stop_words():
    filename = "parasite.csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            stop_words.append(row[0])
    return stop_words


# Étape 5

def html_to_text(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text


# Étape 6

def get_attribute_values(html: str, tag: str, attribute: str):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(tag)
    attribute_values = []

    for tag in tags:
        attribute_values.append(tag.get(attribute))

    return attribute_values


# Étape 8

def get_root_domain(url: str):
    try:
        return url.split('/')[2]
    except:
        return url.split('/')[0]


# Étape 9

def get_domain_urls(domain: str, urls: list):
    domain_urls = []
    not_domain_urls = []
    for url in urls:
        # print(f"""{url} : {get_root_domain(url)}""")
        if get_root_domain(url) == domain:
            domain_urls.append(url)

        elif get_root_domain(url) == url:
            if url.startswith('#'):
                pass
            elif url.startswith('mailto:'):
                pass
            elif url.startswith('tel:'):
                pass
            else:
                domain_urls.append(url)

        else:
            not_domain_urls.append(url)
    return {'domain_urls': domain_urls, 'not_domain_urls': not_domain_urls}


# Étape 10

def get_html_from_url(url: str):
    response = requests.get(url)
    return response.text


# Étape 11

def main():
    url = input("Veuillez entrer l'URL de la page à analyser : ")
    html = get_html_from_url(url)
    text = html_to_text(html)
    words = text_to_words(text)
    words = remove_stop_words(words, get_stop_words())
    firsts_words = list(words.keys())[:3]
    print("\nLes 3 premiers mots clés sont :")
    for word in firsts_words:
        print(f"  -  {word} : {words[word]} fois")

    root_url = get_root_domain(url)
    links = get_attribute_values(html, 'a', 'href')
    domain_urls = get_domain_urls(root_url, links)
    print(f"Nombre de liens entrants : {len(domain_urls['domain_urls'])}")
    print(f"Nombre de liens sortants : {len(domain_urls['not_domain_urls'])}")
    alt_tags = get_attribute_values(html, 'img', 'alt')
    print(f"Nombre de balises alt : {len(alt_tags)}")


if __name__ == "__main__":
    main()
