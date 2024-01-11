import streamlit as st
from algorithms.word_representation import word_representation
from algorithms.word_embedding import word_embedding
from algorithms.pos_tagging import pos_tagging
from algorithms.ner_representation import ner_representation
from algorithms.dependency_parsing import dependency_parsing
from algorithms.keyword_extractor import keyword_extractor
from algorithms.topic_modeling import topic_modeling
from algorithms.text_visualizer import text_visualizer
from algorithms.text_analysis import text_analysis
from algorithms.text_summarization import text_summarization
from algorithms.language_translator import language_translator


def algos():
    tasks_menu = [
        "Word Representation",
        "Word Embedding",
        "Part of Speech Tagging",
        "Named Entity Recognition",
        "Dependency Parsing",
        "Topic Modeling",
        "Keyword Extraction",
        "Text Visualization",
        "Text Analysis",
        "Text Summarization",
        "Language Translation",
    ]

    # user choice
    choice = st.sidebar.selectbox("NLP Tasks", tasks_menu)

    # nlp tasks
    if choice == "Word Representation":
        word_representation()

    elif choice == "Word Embedding":
        word_embedding()

    elif choice == "Part of Speech Tagging":
        pos_tagging()

    elif choice == "Named Entity Recognition":
        ner_representation()

    elif choice == "Dependency Parsing":
        dependency_parsing()

    elif choice == "Topic Modeling":
        topic_modeling()

    elif choice == "Keyword Extraction":
        keyword_extractor()

    elif choice == "Text Visualization":
        text_visualizer()

    elif choice == "Text Analysis":
        text_analysis()

    elif choice == "Text Summarization":
        text_summarization()

    elif choice == "Language Translation":
        language_translator()
