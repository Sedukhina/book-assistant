'''import re
import spacy

def extract_links(text):
    link_pattern = r'https?://\S+|ftp://\S+|www\.\S+|(?:\b\w+\.\w+\b)'
    links = re.findall(link_pattern, text)
    text = re.sub(link_pattern, '', text)
    return links, text


def process_query(query_text):
    links, text = extract_links(query_text)
    # Loading language model
    nlp = spacy.load("en_core_web_sm")
    # Tokenization, POS tagging, Named Entity Recognition, Lemmatization
    query_doc = nlp(text)
'''
