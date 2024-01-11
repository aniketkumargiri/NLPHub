import streamlit as st
import docx2txt
import pdfplumber
import spacy
from spacy import displacy


def show_dependency_parsing(text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(text)
    html_output = displacy.render(docx, style="dep")
    html_with_style = f'<div style="width: 100px; height: 50px">{html_output}</div>'
    st.markdown(html_with_style, unsafe_allow_html=True)


def dependency_parsing_techniques(input_text):
    if st.button("Show Dependency Parsing"):
        st.success("Dependency Parsing Using Spacy (displacy)")
        show_dependency_parsing(input_text)


def dependency_parsing():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Dependency Parsing NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        dependency_parsing_techniques(input_text)

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
            dependency_parsing_techniques(text_file)
