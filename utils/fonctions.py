import streamlit as st
import base64
import emoji
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen
import spacy

def analyze_text(doc, anonymize, selected_entities):

    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append((token.text, "Person", "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append((token.text, "Location", "#fda"))
        elif (token.ent_type_ in ["ORG"]) & ("ORG" in selected_entities):
            tokens.append((token.text, "Organization", "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    if anonymize:
        anonymized_tokens = []
        for token in tokens:
            if type(token) == tuple:
                token = ("X" * len(token[0]), token[1], token[2])

            anonymized_tokens.append(token)
        return anonymized_tokens

    else:
        return tokens


def load_models():
    print("loading models")
    fr_model = spacy.load("./models/fr", disable=["parser", "tagger"])
    en_model = spacy.load("./models/en", disable=["parser", "tagger"])
    models = {"fr": fr_model, "en": en_model}
    return models


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

def expresion(result):
	if  0 < result <= 0.35:
		custom_emoji = ':smile:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif  0.35 < result <= 0.65:
		custom_emoji = ':smile:'*2
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif  0.65 < result:
		custom_emoji = ':smile:'*3
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif  -0.35 <= result < 0.0:
		custom_emoji = ':disappointed:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif  -0.65 <= result < -0.35:
		custom_emoji = ':disappointed:'*2
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif result < -0.65:
		custom_emoji = ':disappointed:'*3
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	else:
		st.write(emoji.emojize(':expressionless:',use_aliases=True))
	st.info("Polarity Score is:: {}".format(result))
