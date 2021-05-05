import streamlit as st
st.set_page_config(page_title=' 🙂 ☹ Analysis',page_icon=" ")

from utils.ui import (
	side,
	sentiment,
	text_analysis_from_url,
	NER,
	NER_from_url,
)



# Fetch Text From Url

def main():
	"""Sentiment and NER Analysis App """

	st.title("Sentiment and NER Analysis App")

	activities = ["NER from URL","NER","Sentiment Analysis","Sentiment Analysis on URL","About"]
	choice = st.sidebar.selectbox("Choice",activities)

	if choice == 'Sentiment Analysis':
		sentiment()

	if choice == 'Sentiment Analysis on URL':
		text_analysis_from_url()

	if choice == 'NER':
		NER()

	if choice == 'NER from URL':
		NER_from_url()

	if choice == 'About':
		st.subheader("About : Sentiment and NER Analysis App")
		st.info("Built with Streamlit, Textblob, annotated_text, spacy  and  Emoji")
		st.text("This version is in English")
		side()

if __name__ == '__main__':
	main()
