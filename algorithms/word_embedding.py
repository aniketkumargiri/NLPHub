import streamlit as st
import pandas as pd
import docx2txt
import pdfplumber
from gensim.models import Word2Vec, FastText

VECTOR_SIZE = 50


def preprocess_text(text):
    # tokenizing the text into sentences & then sentences into words/tokens
    tokens_list = [[token for token in sent.split()] for sent in text.split(".")]
    return tokens_list


def skipgram_gensim(sentences):
    # Skip-gram model using Gensim
    skipgram_model = Word2Vec(
        sentences, vector_size=VECTOR_SIZE, sg=1, window=5, min_count=1
    )
    # extracting vocabulary
    vocabulary = skipgram_model.wv.index_to_key
    # extracting word vectors
    word_vectors = [skipgram_model.wv[word] for word in vocabulary]
    # converting to DataFrame
    embedding_df = pd.DataFrame(word_vectors, index=vocabulary)

    return embedding_df


def cbow_gensim(sentences):
    # CBOW model using Gensim
    cbow_model = Word2Vec(
        sentences, vector_size=VECTOR_SIZE, sg=0, window=5, min_count=1
    )
    # extracting vocabulary
    vocabulary = cbow_model.wv.index_to_key
    # extracting word vectors
    word_vectors = [cbow_model.wv[word] for word in vocabulary]
    # converting to DataFrame
    embedding_df = pd.DataFrame(word_vectors, index=vocabulary)

    return embedding_df


def skipgram_fasttext(sentences):
    # Skip-gram model using FastText
    skipgram_model = FastText(
        sentences, vector_size=VECTOR_SIZE, sg=1, window=5, min_count=1
    )
    # extracting vocabulary
    vocabulary = skipgram_model.wv.index_to_key
    # extracting word vectors
    word_vectors = [skipgram_model.wv[word] for word in vocabulary]
    # converting to DataFrame
    embedding_df = pd.DataFrame(word_vectors, index=vocabulary)

    return embedding_df


def cbow_fasttext(sentences):
    # CBOW model using FastText
    cbow_model = FastText(
        sentences, vector_size=VECTOR_SIZE, sg=0, window=5, min_count=1
    )
    # extracting vocabulary
    vocabulary = cbow_model.wv.index_to_key
    # extracting word vectors
    word_vectors = [cbow_model.wv[word] for word in vocabulary]
    # converting to DataFrame
    embedding_df = pd.DataFrame(word_vectors, index=vocabulary)

    return embedding_df


def display_word_embeddings(model, title):
    # displaying the word embeddings
    st.info(f"{title}")
    st.write(model)


def word_embedding_techniques(input_text):
    # input text pre-processing
    tokenized_text = preprocess_text(input_text)

    if st.button("Get Word Embedding"):
        st.success("Generating...")
        # beta expander for two columns: Gensim & FastText
        left_column, right_column = st.columns(2)

        # Gensim Skip-gram & CBOW
        with left_column:
            st.write("##### Gensim : Skip-gram & CBOW")

            with st.expander("Skip-gram"):
                display_word_embeddings(skipgram_gensim(tokenized_text), "Skip-gram")

            with st.expander("CBOW"):
                display_word_embeddings(cbow_gensim(tokenized_text), "CBOW")

        # FastText Skip-gram & CBOW
        with right_column:
            st.write("##### FastText : Skip-gram & CBOW")
            with st.expander("Skip-gram"):
                display_word_embeddings(skipgram_fasttext(tokenized_text), "Skip-gram")

            with st.expander("CBOW"):
                display_word_embeddings(cbow_fasttext(tokenized_text), "CBOW")


def word_embedding():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Word Embedding NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        word_embedding_techniques(input_text)

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
            word_embedding_techniques(text_file)
