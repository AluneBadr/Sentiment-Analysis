import re
import requests
import glob
import itertools
from string import punctuation

import pandas as pd

urls = [
    #"https://raw.githubusercontent.com/stopwords-iso/stopwords-fr/master/stopwords-fr.txt",
    "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt"
]


def download_stopwords(url):
    response = requests.get(url)
    stopwords = response.content.decode('utf-8').split("\n")
    return stopwords


def get_stopwords():
	STOPWORDS = ['the','s']
	for url in urls:
		STOPWORDS += download_stopwords(url)
	return STOPWORDS

STOPWORDS = get_stopwords()


def strip_url(text):
    return re.sub(r"http\S+", "", text)

def strip_tags(text):
    return re.sub(r'<[^>]+>', "", text)

def strip_dates(text):
    regex = r"\d{1,2}/\d{1,2}/\d{4}"
    text = re.sub(regex, '', text)
    return text

def strip_brackets(text):
    text = re.sub(r"\[.*?\]", '', text)
    return text

def strip_hyphens(text):
    text = re.sub(r"\-\-+", "", text)
    return text

def strip_expressions(text, expressions):
    for expression in expressions:
        text = re.sub(expression, "", text)
    return text

def strip_stopwords(text, stopwords):
	text = ' '.join([i for i in text.split(' ') if (i.strip() not in stopwords and len(i.strip())>2)])
	return text

def strip_emails(text):
    text = re.sub(r"@", "", )
    return text

def clean_text(text):
	text = strip_url(text)
	text = strip_tags(text)
	text = strip_dates(text)
	text = strip_brackets(text)
	text = strip_hyphens(text)
	text = strip_stopwords(text, STOPWORDS)
	return text






def clean_tokens(tokens_with_entities):
    tokens = [token.lower() for (token, entity) in tokens_with_entities if entity == ""]     
    tokens = [token for token in tokens if token.strip() != ""]
    tokens = [token for token in tokens if token not in punctuation]
    tokens = [token for token in tokens if len(token) > 1]
    tokens = [token for token in tokens if len(token) < 20]
    tokens = [token for token in tokens if not token.isdigit()]
    tokens = [token for token in tokens if not token.startswith("http")]
    tokens = [token for token in tokens if re.search(
        r"[^a-zA-Z_éàèùâêîôûçëïü']+", token) is None]
    tokens = [token for token in tokens if not token.endswith("'")]
    tokens = [token for token in tokens if token.strip() not in STOPWORDS]
    return tokens



def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    cleantext = re.sub('-', ' ', cleantext)
    cleantext = re.sub('\*', '', cleantext) 
    cleantext = re.sub('\xa0', ' ', cleantext)

    return cleantext


    
#re.match("(.*?):",string).group()



#re.search(r"Message:\s(.*)", mes).group(1)


