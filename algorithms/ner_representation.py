import streamlit as st
import spacy
from spacy import displacy
import docx2txt
import pdfplumber


def ner_highlighting(text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(text)
    html_output = displacy.render(docx, style="ent")
    st.write(html_output, unsafe_allow_html=True)


def ner_techniques(input_text):
    if st.button("Highlight NER"):
        st.success("Named Entity Recognition Using Spacy (displacy)")
        ner_highlighting(input_text)
        st.markdown("<br>" * 2, unsafe_allow_html=True)


def ner_representation():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Named Entity Recognition NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        ner_techniques(input_text)

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
            ner_techniques(text_file)
