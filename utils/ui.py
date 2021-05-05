import streamlit  as st
from annotated_text import annotated_text
import datetime
# NLP Pkgs
import nltk
from textblob import TextBlob
import pandas as pd
# Emoji
import emoji
import spacy
#from spacy import displacy

from utils import SessionState, process

from utils.fonctions import (
    local_css,
    img_to_bytes,
    get_text,
	expresion,
    analyze_text,
    load_models,
)

import plotly.graph_objects as go
import plotly.express as px

models = load_models()


def side():
    local_css('./css/styles.css')
    st.markdown("---")
    st.markdown(
    """<div id="img-container">
        <img src='data:image/png;base64,{}' class='img-fluid' width=200 height=200>
        <h1>KA Alioune</h1>
        <div class="images">
            <a href="https://github.com/AluneBadr" target="_blank"><img src="data:image/png;base64,{}"/></a>
            <a href="https://www.linkedin.com/in/alioune-ka-017351171/" target="_blank"><img src="data:image/png;base64,{}"/></a>
        </div>
    </div>""".format(img_to_bytes("./image/Image1.png"),
                     img_to_bytes("./image/github.png"),
                     img_to_bytes("./image/linkedin.png")
                     ),unsafe_allow_html=True)

    st.markdown(
        """<div id="bio-info">
        <h3> Data Scientist / Engineer </h3>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        """<div id="bio-contact">
        <p>
            📧 : aliouneka95@outlook.fr <br/>
            📞 : 0658262149 <br/>
            🏠 : 12 Rue Nicolas Copernic 27000, Evreux
        </p>
         <br/>
    </div>""", unsafe_allow_html=True)

def sentiment():
    st.subheader("Sentiment Analysis")
    st.write(emoji.emojize('Everyone ❤️  Streamlit ',use_aliases=True))
    raw_text = st.text_area("Enter Your Text","Type here (English)")
    if st.button("Analyze"):
        st.write("Cleaned text : ")
        st.write(process.clean_text(raw_text))
        blob = TextBlob(raw_text)
        result = blob.sentiment.polarity
        expresion(result)

def text_analysis_from_url():
    session_state = SessionState.get(name="", Analyze=False)
    st.subheader("Sentiment Analysis From URL")
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

def NER():
    st.subheader("Named Entity Recog with Spacy")

    selected_language = st.sidebar.selectbox("Select a language", ("en", "fr"))
    selected_model = models[selected_language]
    selected_entities = st.sidebar.multiselect(
	    "Select entities to detect",
	    ["ORG", "PER", "LOC"],
	    default=["ORG", "PER", "LOC"],
	)
    session_state = SessionState.get(name="", Analyze=False)
    session_state.raw_text = st.text_area("Enter Text Here","Type Here")
    #text_preview_length = st.slider("Length to Preview",50,100)
    Analyze = st.button("Analyze")
    if Analyze:
        session_state.Analyze = True
    if session_state.Analyze:
        doc = selected_model(session_state.raw_text)
        anonymize = st.checkbox("Anonymize")
        tokens = analyze_text(doc, anonymize, selected_entities)
        annotated_text(*tokens, height=1000)
		#html = displacy.render(docx,style="ent")
		#html = html.replace("\n\n","\n")
        #st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

def NER_from_url():
    ss = SessionState.get(name="", Analyze=False)
    st.subheader("Named Entity Recog with Spacy")
    ss.raw_url = st.text_input("Enter URL Here","https://en.wikipedia.org/wiki/Donald_Trump")
    #text_preview_length = st.slider("Length to Preview",50,100)
    Analyze = st.button("Analyze", key=200)
    if Analyze:
        ss.Analyze = True
    if ss.Analyze:
        if ss.raw_url != "Type here (English)":
            #st.write(process.get_stopwords())
            raw_text = get_text(ss.raw_url)
            try:
                raw_text = raw_text[:1000]
            except:
                raw_text = raw_text
            selected_language = st.sidebar.selectbox("Select a language", ("en", "fr"))
            selected_model = models[selected_language]
            selected_entities = st.sidebar.multiselect(
        	    "Select entities to detect",
        	    ["ORG", "PER", "LOC"],
        	    default=["ORG", "PER", "LOC"],
        	)

            doc = selected_model(raw_text)
            anonymize = st.checkbox("Anonymize")
            tokens = analyze_text(doc, anonymize, selected_entities)
            annotated_text(*tokens,height=1000)
