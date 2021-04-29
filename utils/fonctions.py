import streamlit as st
import base64
import emoji
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen
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
