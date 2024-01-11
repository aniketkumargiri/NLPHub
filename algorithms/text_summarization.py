import streamlit as st
import docx2txt
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def preprocessed_text(docx):
    # parsing from string and using english tokenization
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))

    return parser.document


def luhn_summarization(parsed_docx, num_paras):
    luhn_summarizer = LuhnSummarizer()
    summary_setences = luhn_summarizer(parsed_docx, num_paras)

    summary = ""
    for sent in summary_setences:
        summary = summary + str(sent)
    return summary


def lsa_summarization(parsed_docx, num_paras):
    lsa_summarizer = LsaSummarizer()
    summary_setences = lsa_summarizer(parsed_docx, num_paras)

    summary = ""
    for sent in summary_setences:
        summary = summary + str(sent)
    return summary


def textrank_summarization(parsed_docx, num_paras):
    textrank_summarizer = TextRankSummarizer()
    summary_setences = textrank_summarizer(parsed_docx, num_paras)

    summary = ""
    for sent in summary_setences:
        summary = summary + str(sent)
    return summary


def lexrank_summarization(parsed_docx, num_paras):
    lexrank_summarizer = LexRankSummarizer()
    summary_setences = lexrank_summarizer(parsed_docx, num_paras)

    summary = ""
    for sent in summary_setences:
        summary = summary + str(sent)
    return summary


def text_summarization_techniques(input_text):
    if st.button("Summarize"):
        st.success("Text Summarization Using Sumy")

        # parser + tokenizer
        parsed_docx = preprocessed_text(input_text)

        left, right = st.columns(2)

        with left.expander("Luhn Summarizer"):
            st.info("Based on Frequency of Most Important Words")
            summary = luhn_summarization(parsed_docx, 2)
            st.write(summary)

        with left.expander("LSA Summarizer"):
            st.info("Based on Term Frequency with Singular Value Decomposition")
            summary = lsa_summarization(parsed_docx, 2)
            st.write(summary)

        with right.expander("TextRank Summarizer"):
            st.info(
                "Graph Based Page Rank Algorithm to find the Most Relevant Sentences"
            )
            summary = textrank_summarization(parsed_docx, 2)
            st.write(summary)

        with right.expander("LexRank Summarizer"):
            st.info(
                "Based on Eigen Vector Centrality & Similarity Matrix using Cosine Similarity"
            )
            summary = lexrank_summarization(parsed_docx, 2)
            st.write(summary)


def text_summarization():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Text Summarizer NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        text_summarization_techniques(input_text)

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
            text_summarization_techniques(text_file)
