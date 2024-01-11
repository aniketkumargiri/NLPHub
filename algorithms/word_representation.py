import streamlit as st
import pandas as pd
import docx2txt
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def one_hot_encoding(document):
    # Using binary bag of words
    count_vectorizer = CountVectorizer(binary=True)
    count_vectors = count_vectorizer.fit_transform(document.split("."))
    count_df = pd.DataFrame(
        count_vectors.toarray(), columns=count_vectorizer.get_feature_names_out()
    )
    st.write(count_df)

    st.warning("Bar Chart Plot for One Hot Encoding:")
    st.bar_chart(count_df, use_container_width=True)


def bag_of_words(document):
    # Using count vectorization (bag of words)
    bow_vectorizer = CountVectorizer()
    bow_vectors = bow_vectorizer.fit_transform(document.split("."))
    bow_df = pd.DataFrame(
        bow_vectors.toarray(), columns=bow_vectorizer.get_feature_names_out()
    )
    st.write(bow_df)

    st.warning("Bar Chart Plot for Bag Of Words:")
    st.bar_chart(bow_df, use_container_width=True)


def term_frequency_inverse_document_frequency(document):
    # Using TF-IDF vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectors = tfidf_vectorizer.fit_transform(document.split("."))
    tfidf_df = pd.DataFrame(
        tfidf_vectors.toarray(), columns=tfidf_vectorizer.get_feature_names_out()
    )
    st.write(tfidf_df)

    st.warning("Bar Chart Plot for TFIDF:")
    st.bar_chart(tfidf_df, use_container_width=True)


def word_representation_techniques(input_text):
    # word representation techniques
    vectorization_techniques = ["One Hot Encoding", "Bag Of Words", "TF-IDF Vectorizer"]

    # dropdown to select the word representation technique
    selected_vectorization = st.selectbox(
        "Word Representation Techniques", vectorization_techniques
    )

    if st.button("Get Word Representation"):
        if selected_vectorization == "One Hot Encoding":
            st.success("Word Representation Using Binary Bag Of Words")
            one_hot_encoding(input_text)

        elif selected_vectorization == "Bag Of Words":
            st.success("Word Representation Using Count Vectorizer")
            bag_of_words(input_text)

        elif selected_vectorization == "TF-IDF Vectorizer":
            st.success("Term Frequency - Inverse Document Frequency Vectorization")
            term_frequency_inverse_document_frequency(input_text)


def word_representation():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Word Representation NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        word_representation_techniques(input_text)

    elif choice == "Drop Files":
        raw_text_file = st.file_uploader("Upload File Here", type=["docx", "pdf"])
        file_type_list = st.selectbox("FileType", ["docx", "pdf"])

        if raw_text_file is not None:
            if file_type_list == "docx":
                text_file = docx2txt.process(raw_text_file)

            elif file_type_list == "pdf":
                with pdfplumber.open(raw_text_file) as pdf_file:
                    pages = pdf_file.pages[0]
                    text_file = pages.extract_text()

            # st.write(text_file)
            word_representation_techniques(text_file)
