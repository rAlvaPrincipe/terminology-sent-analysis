import streamlit as st
from models import Model
from sentiment_analysis import Sentiment
from semantic_analysis import Sematics
from es import ES
import pandas as pd
st.set_page_config(layout="wide", page_title="Sentiment Analysis")
from lemmatizer import tint, get_lemmas
from definitions import get_meanings


@st.cache_resource()
def load_models():
    models = Model()
    sentiment = Sentiment(models)
    semantics = Sematics(models)
    es = ES()
    words = words = [ el["id"] for el in es.get_all_docs(["word"], None, ["word"])]
    return models, sentiment, semantics, es, words
    
    
models, sentiment, semantics, es, words = load_models()

st.sidebar.image(
    "./logo.jpeg",
    width=270,
)

categories = ["Data Ingestion", "Sentiment", "Semantics", "Bonus"]
selected_category = st.sidebar.selectbox("Select Category", categories)

if selected_category == "Data Ingestion":
    nav = st.sidebar.radio("Select Dashboard", ["Scraping"])
elif selected_category == "Sentiment":
    nav = st.sidebar.radio("Select Dashboard", ["Sentiment 1", "Sentiment 2"])
elif selected_category == "Semantics":
    nav = st.sidebar.radio("Select Dashboard", ["Employees Agreement", "Similarity Among Definitions"])
elif selected_category == "Bonus":
    nav = st.sidebar.radio("Select Dashboard", ["Analyze a New Definition", "Employees Coherence"])
    



if nav == "Scraping":
    st.title("Scraping")
    input_word = st.text_input("insert a word in italian", "botte")
    if st.button("Go!"):
        col1, col2, col3 = st.columns([10, 1, 10])
        tint_resp = tint(input_word)
        lemmas = get_lemmas(tint_resp)
        with col1:
            st.image("tint.png",width=100)
            st.json(lemmas)
            with st.expander("Full Tint response"):
                st.json(tint_resp)
        with col3:
            st.image("treccani.png",width=300)
            for lemma in lemmas:
                with st.expander(lemma):
                    st.json(get_meanings(lemma, 1))
            
elif nav == "Sentiment 1":
    st.plotly_chart(sentiment.comparison_sentiment_embedders(),  use_container_width=True, theme="streamlit", height=800)
        
elif nav == "Sentiment 2":
    pl1, pl2 = sentiment.get_sent()
    tab1, tab2 = st.tabs(["Person Wise", "Word Wise"])
    with tab1: 
        st.plotly_chart(pl1,  use_container_width=True, theme=None)
    with tab2: 
        st.plotly_chart(pl2,  use_container_width=True, theme=None)

    
elif nav == "Employees Agreement":
    pl1, pl2 = semantics.concept()
    tab1, tab2, tab3 = st.tabs(["Treccani", "Custom (Person Wise)", " Custom (Word Wise)"])
    with tab1: 
        num_words = st.slider('Choose the number of random definitions to visualize', 0, 1000, 250)
        if st.button("Go!"):
            st.plotly_chart(semantics.mod_1(num_words),  use_container_width=True, theme=None)
    with tab2: 
        st.plotly_chart(pl1,  use_container_width=True, theme=None)
    with tab3: 
        st.plotly_chart(pl2,  use_container_width=True, theme=None)

    
elif nav == "Similarity Among Definitions": 
    col_a, col_b = st.columns([10,2]) 
    l=[] 
    
    with col_b:
        tmp = st.selectbox('Pre-fill demo', ["None", "human-machine", "ownership", "evangelismo", "abandonware", "opinionated", "braggiotti", "alva", "sgarro", "chiarini", "dondi", "gamondi", "sperto", "cambieri"])
        if tmp == "None":
            l = []
        elif tmp == "human-machine":
            l = ["software_1", "intelligenza_1", "elaborare_1", "macchina_1", "sentimento_1", "ragionare_1", "logica_1", "istinto_1", "processare_1", "amore_1", "morte_1", "decidere_1", "sorridere_1", "salute_1", "algoritmo_1", "scienza_1"]
        elif tmp == "ownership":
            l = ["ownership_braggiotti_1", "ownership_alva_1", "ownership_sgarro_1", "ownership_chiarini_1", "ownership_dondi_1", "ownership_gamondi_1", "ownership_sperto_1", "ownership_cambieri_1"] 
        elif tmp == "evangelismo":
            l = ["evangelismo_braggiotti_1", "evangelismo_alva_1", "evangelismo_sgarro_1", "evangelismo_chiarini_1", "evangelismo_dondi_1", "evangelismo_gamondi_1", "evangelismo_sperto_1", "evangelismo_cambieri_1"] 
        elif tmp == "abandonware":
            l = ["abandonware_braggiotti_1", "abandonware_alva_1", "abandonware_sgarro_1", "abandonware_chiarini_1", "abandonware_dondi_1", "abandonware_gamondi_1", "abandonware_sperto_1", "abandonware_cambieri_1"] 
        elif tmp == "opinionated":
            l = ["opinionated_braggiotti_1", "opinionated_alva_1", "opinionated_sgarro_1", "opinionated_chiarini_1", "opinionated_dondi_1", "opinionated_gamondi_1", "opinionated_sperto_1", "opinionated_cambieri_1"] 
        elif tmp == "braggiotti":
            l = ["ownership_braggiotti_1", "abandonware_braggiotti_1", "opinionated_braggiotti_1", "evangelismo_braggiotti_1"] 
        elif tmp == "alva":
            l = ["ownership_alva_1", "abandonware_alva_1", "opinionated_alva_1", "evangelismo_alva_1"] 
            
        elif tmp == "sgarro":
            l = ["ownership_sgarro_1", "abandonware_sgarro_1", "opinionated_sgarro_1", "evangelismo_sgarro_1"] 
        elif tmp == "chiarini":
            l = ["ownership_chiarini_1", "abandonware_chiarini_1", "opinionated_chiarini_1", "evangelismo_chiarini_1"] 
        elif tmp == "dondi":
            l = ["ownership_dondi_1", "abandonware_dondi_1", "opinionated_dondi_1", "evangelismo_dondi_1"] 
        elif tmp == "gamondi":
            l = ["ownership_gamondi_1", "abandonware_gamondi_1", "opinionated_gamondi_1", "evangelismo_gamondi_1"] 
        elif tmp == "sperto":
            l = ["ownership_sperto_1", "abandonware_sperto_1", "opinionated_sperto_1", "evangelismo_sperto_1"]                                   
        elif tmp == "cambieri":
            l = ["ownership_cambieri_1", "abandonware_cambieri_1", "opinionated_cambieri_1", "evangelismo_cambieri_1"]    
    
            
    with col_a:
        selected_words = st.multiselect('Choose one or more definitions to analyze:', words, l)

    scope = st.selectbox("Scope:", ["all definitions", "custom definitions", "Treccani definitions"])
    if st.button("Go!"):
        col1, col2 = st.columns([3, 3])
        
        docs, dfs, fig = semantics.mod_3(selected_words, scope)
        with col1:
            for doc, df, selected_word  in zip(docs, dfs, selected_words):
                with st.expander(selected_word):
                    st.json({"definition":doc}, expanded=False)
                    st.dataframe(df)
                    
        with col2:
            st.plotly_chart(fig,  use_container_width=True, theme="streamlit", height=800)
            
elif nav == "Analyze a New Definition":
    input_def = st.text_input("Write a definition:")
    scope = st.selectbox("Scope:", ["all definitions", "custom definitions", "Treccani definitions"])
    if st.button("Go!"):
        df = semantics.mod_4(input_def, scope)
        st.dataframe(df)

elif nav == "Employees Coherence":
    employee = st.selectbox("Select an Employee", ["braggiotti", "sgarro", "chiarini", "dondi", "gamondi", "sperto", "cambieri"])
    
    dfs, fig = semantics.employee_coherence(employee)
    st.plotly_chart(fig,  use_container_width=True, theme="streamlit", height=800)


    for key in dfs.keys():
        with st.expander(key):
            col1, col2 = st.columns([3, 3])
            with col1:
                st.caption(dfs[key][0]["doc"])
                st.dataframe(dfs[key][0]["df"])
            with col2:
                st.caption(dfs[key][1]["doc"])
                st.dataframe(dfs[key][1]["df"])
                