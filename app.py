import streamlit as st
st.set_page_config(page_title=' 🙂 ☹ Analysis',page_icon=" ")

# NLP Pkgs
import nltk
nltk.data.path.append('./nltk_data/')
from textblob import TextBlob
import pandas as pd 
# Emoji
import emoji

from utils import SessionState, process
from utils.fonctions import(
	get_text,
	expresion,
	)
from utils.ui import side


import plotly.graph_objects as go
import plotly.express as px
# Fetch Text From Url

def main():
	"""Sentiment Analysis Emoji App """

	st.title("Sentiment Analysis Emoji App")

	activities = ["Sentiment","Text Analysis on URL","About"]
	choice = st.sidebar.selectbox("Choice",activities)

	if choice == 'Sentiment':
		st.subheader("Sentiment Analysis")
		st.write(emoji.emojize('Everyone ❤️  Streamlit ',use_aliases=True))
		raw_text = st.text_area("Enter Your Text","Type here (English)")
		if st.button("Analyze"):
			st.write("Cleaned text : ")
			st.write(process.clean_text(raw_text))
			blob = TextBlob(raw_text)
			result = blob.sentiment.polarity
			expresion(result)
			
	if choice == 'Text Analysis on URL':
		session_state = SessionState.get(name="", Analyze=False)
		st.subheader("Analysis on Text From URL")
		session_state.raw_url = st.text_input("Enter URL Here","https://en.wikipedia.org/wiki/COVID-19_pandemic")
		#text_preview_length = st.slider("Length to Preview",50,100)
		Analyze = st.button("Analyze")
		if Analyze:
			session_state.Analyze = True
		if session_state.Analyze:
			if session_state.raw_url != "Type here (English)":
				#st.write(process.get_stopwords())
				result = get_text(session_state.raw_url)
				blob = TextBlob(process.clean_text(result))
				len_of_full_text = len(result)
				frequency = pd.DataFrame.from_dict(blob.word_counts, orient='index', columns=['count'])
				f = px.bar(frequency.sort_values(by='count', ascending=False)[:30])
				st.plotly_chart(f)
				#len_of_short_text = round(len(result)/text_preview_length)
				st.success("Length of Full Text::{}".format(len_of_full_text))
				#st.success("Length of Short Text::{}".format(len_of_short_text))
				#st.info(result[:len_of_short_text])
				c_sentences = [ sent for sent in blob.sentences ]
				c_sentiment = [sent.sentiment.polarity for sent in blob.sentences]
				
				new_df = pd.DataFrame(zip(c_sentences,c_sentiment),columns=['Sentence','Sentiment_score'])
				
				new_df =  new_df.rename_axis('sentence_n°').reset_index().sort_values(by='Sentiment_score')
				new_df.index = range(0, len(new_df))
				#st.table(new_df)
				#fig = go.Figure(data=go.Scatter(x=new_df.index.values, y=new_df.Sentiment.values,mode='lines+markers')
				#,text=new_df["Sentence"].values , hoverinfo = 'y+text', hovertemplate = "score: %{y:.1f}% | sentence: %{text}")
				
				#fig['layout'].update(height=400, width=900,title="Sentiment Evolution")
				
				fig = px.scatter(
					data_frame=new_df, 
					x=new_df.index.values, 
					y='Sentiment_score', 
					hover_data=[new_df['sentence_n°'], new_df['Sentiment_score']])
				fig.update_layout(
						xaxis_title="Sentence Index",
						title="Sentences sentiment score"
						)
				st.plotly_chart(fig)
				
				n_of_sentence = st.multiselect("Preview particular sentences using its n°",
				range(len(new_df)))
			if st.button("Preview"):
				try:
					sentence = new_df[new_df['sentence_n°'].isin(n_of_sentence)]
					st.table(sentence)
				except:
					st.warning("Can't find sentences ! ")
					#st.write(list(n_of_sentence) )

	if choice == 'About':
		st.subheader("About : Sentiment Analysis App")
		st.info("Built with Streamlit, Textblob  and  Emoji")
		st.text("This version is in English")
		side()

if __name__ == '__main__':
	main()