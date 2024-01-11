import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import docx2txt
import pdfplumber
from collections import Counter
import neattext as nt
import neattext.functions as nfx
from textblob import TextBlob
from wordcloud import WordCloud
import contractions
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import altair as alt
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
matplotlib.use("Agg")


TAGS = {
    "NN": "green",
    "NNS": "green",
    "NNP": "green",
    "NNPS": "green",
    "VB": "blue",
    "VBD": "blue",
    "VBG": "blue",
    "VBN": "blue",
    "VBP": "blue",
    "VBZ": "blue",
    "JJ": "red",
    "JJR": "red",
    "JJS": "red",
    "RB": "cyan",
    "RBR": "cyan",
    "RBS": "cyan",
    "IN": "darkwhite",
    "POS": "darkyellow",
    "PRP$": "magenta",
    "PRP$": "magenta",
    "DET": "black",
    "CC": "black",
    "CD": "black",
    "WDT": "black",
    "WP": "black",
    "WP$": "black",
    "WRB": "black",
    "EX": "yellow",
    "FW": "yellow",
    "LS": "yellow",
    "MD": "yellow",
    "PDT": "yellow",
    "RP": "yellow",
    "SYM": "yellow",
    "TO": "yellow",
    "None": "off",
}


def get_pos_tags(docx):
    blob = TextBlob(docx)
    tagged_docx = blob.tags
    tagged_df = pd.DataFrame(tagged_docx, columns=["tokens", "tags"])
    return tagged_df


def pos_tag_visualizer(tagged_docx):
    colored_text = []
    for i in tagged_docx:
        if i[1] in TAGS.keys():
            token = i[0]
            color_for_tag = TAGS.get(i[1])
            result = '<span style="color:{}">{}</span>'.format(color_for_tag, token)
            colored_text.append(result)

    output = " ".join(colored_text)
    return output


def plot_word_frequency(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    x, y = zip(*most_common_tokens)
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x=list(x), y=list(y), palette="viridis")
    plt.title("Top Word Frequencies")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.show()
    st.pyplot(fig)


def plot_word_frequency_with_altair(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = dict(word_freq.most_common(num))
    word_freq_df = pd.DataFrame(
        {"tokens": most_common_tokens.keys(), "counts": most_common_tokens.values()}
    )
    brush = alt.selection(type="interval", encodings=["x"])
    c = (
        alt.Chart(word_freq_df)
        .mark_bar()
        .encode(
            x="tokens",
            y="counts",
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        )
        .add_selection(brush)
    )
    st.altair_chart(c, use_container_width=True)


def text_preprocessing(text):
    # lower casing
    lowered_text = text.lower()

    # expand contractions
    fixed_text = contractions.fix(lowered_text)

    # removing stopwords
    removed_stopwords = nfx.remove_stopwords(fixed_text)

    # removing urls
    removed_urls = nfx.remove_urls(removed_stopwords)

    # removing handles
    removed_handles = nfx.remove_userhandles(removed_urls)

    # removing punctuations
    removed_puncts = nfx.remove_punctuations(removed_handles)

    # lemmatization
    preprocesses_text = []
    for token in removed_puncts.split():
        lemmatized_word = lemmatizer.lemmatize(token)
        preprocesses_text.append(lemmatized_word)

    st.write(" ".join(preprocesses_text))


def plot_wordcloud(docx):
    mywordcloud = WordCloud().generate(docx)
    plt.imshow(mywordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()


def plot_mendenhall_curve(docx):
    word_length = [len(token) for token in docx.split()]
    word_length_count = Counter(word_length)
    sorted_word_length_count = sorted(dict(word_length_count).items())
    x, y = zip(*sorted_word_length_count)
    mendenhall_df = pd.DataFrame({"tokens": x, "counts": y})
    st.line_chart(mendenhall_df["counts"])


def text_analysis_techniques(input_text):
    if st.button("Text Analyzer"):
        st.success("Complete Textual Analysis")
        left, right = st.columns(2)

        processed_text = nfx.remove_stopwords(input_text)

        with left:
            with st.expander("Original Text"):
                st.info("Input Text")
                st.write(input_text)

            with st.expander("PoS Tagged Text"):
                st.info("Part of Speech Tagging")
                # tagged_docx = get_pos_tags(input_text)
                # st.dataframe(tagged_docx)

                tagged_docx = TextBlob(input_text).tags
                processed_tags = pos_tag_visualizer(tagged_docx)
                stc.html(processed_tags, scrolling=True)

            with st.expander("Plot Word Freq"):
                st.warning("Word Frequency")
                plot_word_frequency_with_altair(processed_text)

        with right:
            with st.expander("Preprocessed Text"):
                st.info("Preprocessed Text")
                text_preprocessing(input_text)

            with st.expander("Wordcloud Plot"):
                st.info("Wordcloud Distribution")
                plot_wordcloud(processed_text)

            with st.expander("Stylometry Curve Plot"):
                st.warning("Mendenhall Curve")
                plot_mendenhall_curve(input_text)


def text_analysis():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Text Analyzer NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        text_analysis_techniques(input_text)

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
            text_analysis_techniques(text_file)
