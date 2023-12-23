from collections import Counter
import csv
from time import sleep

from bs4 import BeautifulSoup
import requests

class WebPageAnalyzer:
    def __init__(self, url: str, keywords: list = []):
        self.url = url
        self.keywords = keywords
        self.stop_words = []
        self.get_stop_words()

    def text_to_words(self, text: str):
        # rprint(text)
        array_of_words = text.lower().split()
        sorted_word_count = dict(sorted(Counter(array_of_words).items(), key=lambda x: x[1], reverse=True))
        return sorted_word_count

    def remove_stop_words(self, word_dict: dict):
        for word in self.stop_words:
            if word in word_dict:
                del word_dict[word]
        return word_dict

    def get_stop_words(self):
        filename = "parasite.csv"
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.stop_words.append(row[0])

    def html_to_text(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        return text

    def get_attribute_values(self, html: str, tag: str, attribute: str = None):
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all(tag)
        attribute_values = []

        for tag in tags:
            if attribute:
                if tag.get(attribute) != '' and tag.get(attribute) is not None:
                    attribute_values.append(tag.get(attribute))
            else:
                attribute_values.append(tag)

        return attribute_values

    def get_root_domain(self, url: str):
        try:
            return url.split('/')[2]
        except:
            return url.split('/')[0]

    def get_domain_urls(self, domain: str, urls: list):
        domain_urls = []
        not_domain_urls = []

        for i in range(len(urls)):
            if urls[i] == '/':
                urls[i] = f"https://{domain}"
        
        for url in urls:
            if self.get_root_domain(url) == domain or self.get_root_domain(url) == 'www.' + domain or url.startswith('/') :
                domain_urls.append(url)
            elif self.get_root_domain(url) == url:
                if url.startswith('#') or url.startswith('mailto:') or url.startswith('tel:'):
                    pass
                else:
                    domain_urls.append(url)
            else:
                not_domain_urls.append(url)
        return {'domain_urls': domain_urls, 'not_domain_urls': not_domain_urls}

    def get_html_from_url(self, url: str):
        response = requests.get(url)
        return response.text
    
    def get_three_first_words(self, words: dict):
        self.words = words
        return list(words.items())[:3]
    
    def get_incoming_links(self, domain_urls: list):
        return domain_urls['domain_urls']

    def get_outgoing_links(self, domain_urls: list):
        return domain_urls['not_domain_urls']
    
    def compare_keywords(self, words: list):

        target_in_words = 0

        for target_keyword in self.keywords:
            for word in words:
                if target_keyword == word[0]:
                    target_in_words += 1
                else:
                    pass
        
        if target_in_words == 3:
            return True
        else:
            return False

    def main(self):
        html = self.get_html_from_url(self.url)
        text = self.html_to_text(html)
        words = self.text_to_words(text)
        words = self.remove_stop_words(words)
        firsts_words = self.get_three_first_words(words)
        root_url = self.get_root_domain(self.url)
        links = self.get_attribute_values(html, 'a', 'href')
        domain_urls = self.get_domain_urls(root_url, links)
        incoming_links = self.get_incoming_links(domain_urls)
        outgoing_links = self.get_outgoing_links(domain_urls)
        keywords = self.compare_keywords(firsts_words)


        alt_tags = self.get_attribute_values(html, 'img', 'alt')
        all_imgs = self.get_attribute_values(html, 'img')


        return {
            'firsts_words': firsts_words,
            'incoming_links': incoming_links,
            'outgoing_links': outgoing_links,
            'alt_tags': alt_tags,
            'all_imgs': all_imgs,
            'keywords': keywords
        }