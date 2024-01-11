import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk import word_tokenize, pos_tag
import spacy
from spacy import displacy
import docx2txt
import pdfplumber
from textblob import TextBlob
from yellowbrick.text import PosTagVisualizer
from yellowbrick.text.base import TextVisualizer

import warnings

warnings.filterwarnings("ignore")

st.set_option("deprecation.showPyplotGlobalUse", False)


class PosTagTextVisualizer(TextVisualizer):
    """
    A part-of-speech tag visualizer colorizes text to enable
    the user to visualize the proportions of nouns, verbs, etc.
    and to use this information to make decisions about token tagging,
    text normalization (e.g. stemming vs lemmatization),
    vectorization, and modeling.

    Parameters
    ----------
    kwargs : dict
        Pass any additional keyword arguments to the super class.
    cmap : dict
        ANSII colormap

    These parameters can be influenced later on in the visualization
    process, but can and should be set as early as possible.
    """

    def __init__(self, ax=None, **kwargs):
        """
        Initializes the base frequency distributions with many
        of the options required in order to make this
        visualization work.
        """
        super(PosTagTextVisualizer, self).__init__(ax=ax, **kwargs)

        # TODO: hard-coding in the ANSI colormap for now.
        self.COLORS = {
            "white": "\033[0;37m{}\033[0m",
            "yellow": "\033[0;33m{}\033[0m",
            "green": "\033[0;32m{}\033[0m",
            "blue": "\033[0;34m{}\033[0m",
            "cyan": "\033[0;36m{}\033[0m",
            "red": "\033[0;31m{}\033[0m",
            "magenta": "\033[0;35m{}\033[0m",
            "black": "\033[0;30m{}\033[0m",
            "darkwhite": "\033[1;37m{}\033[0m",
            "darkyellow": "\033[1;33m{}\033[0m",
            "darkgreen": "\033[1;32m{}\033[0m",
            "darkblue": "\033[1;34m{}\033[0m",
            "darkcyan": "\033[1;36m{}\033[0m",
            "darkred": "\033[1;31m{}\033[0m",
            "darkmagenta": "\033[1;35m{}\033[0m",
            "darkblack": "\033[1;30m{}\033[0m",
            None: "\033[0;0m{}\033[0m",
        }

        self.TAGS = {
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
            "DT": "black",
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

    def colorize(self, token, color):
        """
        Colorize text

        Parameters
        ----------
        token : str
            A str representation of

        """
        return f'<span style="color: {color};">{token}</span>'

    def transform(self, tagged_tuples):
        """
        The transform method transforms the raw text input for the
        part-of-speech tagging visualization. It requires that
        documents be in the form of (tag, token) tuples.

        Parameters
        ----------
        tagged_token_tuples : list of tuples
            A list of (tag, token) tuples

        Text documents must be tokenized and tagged before passing to fit()
        """
        self.tagged = [(self.TAGS.get(tag), tok) for tok, tag in tagged_tuples]

        return " ".join((self.colorize(token, color) for color, token in self.tagged))


# highlighting the pos tags with different colors
def highlight_pos_tags(docx):
    docx_list = word_tokenize(docx)
    tagged_tokens = pos_tag(docx_list)

    # color visualization
    color_visualizer = PosTagTextVisualizer()
    html_output = color_visualizer.transform(tagged_tokens)
    st.write(html_output, unsafe_allow_html=True)


# parts of speech tagging with nltk
def pos_tags_nltk(docx):
    nltk_pos_tags = [[nltk.pos_tag(nltk.word_tokenize(i))] for i in docx.split(".")]
    return nltk_pos_tags


# parts of speech tagging with spacy
def pos_tags_spacy(text):
    nlp = spacy.load("en_core_web_sm")
    docs = nlp(text)
    pos_tags_spacy = [
        [[(token.text, token.pos_) for token in sent] for sent in docs.sents]
    ]
    return pos_tags_spacy


# parts of speech tagging with textblob
def pos_tags_textblob(text):
    blob = TextBlob(text)
    pos_tags_textblob = [(word, pos) for word, pos in blob.tags]
    return pos_tags_textblob


# method to plot POS tags
def plot_pos_tags(tagged_docx):
    pos_visualizer = PosTagVisualizer()
    pos_visualizer.fit(tagged_docx)
    pos_visualizer.show()
    st.pyplot()


def plot_textblob_postags(tagged_docx):
    x = []
    y = []
    for word, index in tagged_docx:
        x.append(word)
        y.append(index)

    st.info("Words Vs Pos Tags Using TextBlob")
    # dataframe: word with corresponding tags
    df = pd.DataFrame({"Word": x, "POS_Tag": y})
    st.write(df)

    # plot: word : pos_tag
    palette = sns.color_palette("husl", n_colors=len(df["POS_Tag"].unique()))
    plt.figure(figsize=(10, 5))
    scatter = sns.scatterplot(
        data=df,
        x=df.index,
        y="Word",
        hue="POS_Tag",
        palette=palette,
        legend="full",
        marker="o",
        s=100,
    )

    st.success("Part of Speech Tags Visualization Using TextBlob")
    scatter.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="POS Tag")
    plt.title("Words with Corresponding POS Tags")
    plt.xlabel("Index")
    plt.ylabel("Word")
    st.pyplot(plt)


def pos_tagging_techniques(input_text):
    if st.button("Generate POS Tags"):
        # highlighting pos tags in different colors
        highlight_pos_tags(input_text)

        with st.expander("NLTK POS Tagger"):
            # NLTK POS tagging
            nltk_pos_tags = pos_tags_nltk(input_text)
            st.write(nltk_pos_tags)

            st.success("Part of Speech Tags Visualization Using NLTK")
            plot_pos_tags(nltk_pos_tags)

        with st.expander("spaCy POS Tagger"):
            # spaCy POS tagging
            spacy_pos_tags = pos_tags_spacy(input_text)
            st.write(spacy_pos_tags)

            st.success("Part of Speech Tags Visualization Using spaCy")
            plot_pos_tags(spacy_pos_tags)

        with st.expander("TextBlob POS Tagger"):
            # TextBlob POS tagging
            textblob_pos_tags = pos_tags_textblob(input_text)
            st.write(textblob_pos_tags)

            plot_textblob_postags(textblob_pos_tags)


def pos_tagging():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Part Of Speech Tagger NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        pos_tagging_techniques(input_text)

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
            pos_tagging_techniques(text_file)
