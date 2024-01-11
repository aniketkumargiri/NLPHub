import streamlit as st
import pandas as pd
import docx2txt
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake
import yake
from collections import Counter
import neattext.functions as nt
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib

# from spacy_textrank import TextRank4Keyword

matplotlib.use("Agg")


# converting dictionary to Dataframe
def convert_to_df(my_dict):
    df = pd.DataFrame(list(my_dict.items()), columns=["Keyword", "Scores"])
    return df


# def spacy_textrank_extractor(text, num_of_words=30):
#     textRank = TextRank4Keyword()
#     textRank.analyze(text, candidate_pos=["NOUN", "PROPN"], window_size=4)
#     textrank_keywords = textRank.get_keywords(num_of_words)
#     resulting_keywords_as_df = convert_to_df(dict(textrank_keywords))
#     return resulting_keywords_as_df


def tfidf_extractor(text):
    text = text.lower()
    preprocessed_text = nt.remove_stopwords(text)
    tfidf = TfidfVectorizer(ngram_range=(2, 2))
    tfidf.fit(preprocessed_text.split("."))
    resulting_keywords_as_df = pd.DataFrame(
        {"Keyword": tfidf.get_feature_names_out(), "Scores": tfidf.idf_}
    )
    return resulting_keywords_as_df


def yake_extractor(text):
    keyword_extractor_yake = yake.KeywordExtractor()
    keywords_yake = keyword_extractor_yake.extract_keywords(text)
    resulting_keywords_as_df = convert_to_df(dict(keywords_yake))
    return resulting_keywords_as_df


def rake_extractor(text):
    keyword_extractor_rake = Rake()
    keyword_extractor_rake.extract_keywords_from_text(text)
    keywords_rake_inv = keyword_extractor_rake.get_ranked_phrases_with_scores()
    keywords_rake = {v: k for k, v in dict(keywords_rake_inv).items()}
    resulting_keywords_as_df = convert_to_df(dict(keywords_rake))
    return resulting_keywords_as_df


def wordcount_extractor(text):
    # lower casing
    text = text.lower()
    # removing stopwords
    preprocessed_text = nt.remove_stopwords(text)
    # collecting words tokens & their count in the text
    keyword_results = Counter(preprocessed_text.split(" "))
    # most common 10 keywords
    most_common_keywords = keyword_results.most_common(10)
    # converting words:count dictionary to dataframe
    resulting_keywords_as_df = convert_to_df(dict(most_common_keywords))
    # returning the dataframe
    return resulting_keywords_as_df


def display_output(resulting_keywords_as_df):
    # dataframe display
    st.dataframe(resulting_keywords_as_df)

    st.error("Extracted Keywords Vs Scores")
    # bar chart
    my_chart = (
        alt.Chart(resulting_keywords_as_df).mark_bar().encode(x="Keyword", y="Scores")
    )
    st.altair_chart(my_chart)

    # wordcloud visualization
    st.warning("Most Important Extracted Keywords")
    text_for_wordcloud = " ".join(resulting_keywords_as_df["Keyword"].tolist())
    wordcloud = WordCloud().generate(text_for_wordcloud)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()


def show_extracted_keywords(text):
    keyword_extraction_method_list = [
        "TFIDF",
        "Yake",
        "Rake",
        "Word Counts",
        "TextRank",
    ]

    # dropdown to select destination language
    kw_extract_method = st.selectbox(
        "Select Keyword Extraction Method", keyword_extraction_method_list
    )

    if st.button("Extract Keywords"):
        st.success(f"Using: {kw_extract_method} for Keyword Extraction")
        if kw_extract_method == "TextRank":
            # resulting_keywords_as_df = spacy_textrank_extractor(text)
            return

        elif kw_extract_method == "TFIDF":
            resulting_keywords_as_df = tfidf_extractor(text)

        elif kw_extract_method == "Yake":
            resulting_keywords_as_df = yake_extractor(text)

        elif kw_extract_method == "Rake":
            resulting_keywords_as_df = rake_extractor(text)

        else:
            resulting_keywords_as_df = wordcount_extractor(text)

        # displaying final output
        display_output(resulting_keywords_as_df)


def keyword_extractor():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Keyword Extractor NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        show_extracted_keywords(input_text)

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
            show_extracted_keywords(text_file)
