import streamlit as st
import docx2txt
import pdfplumber
import googletrans
from googletrans import Translator


def language_translation_techniques(input_text):
    # list of destination languages
    dest_languages = [
        "Hindi",
        "English",
        "Bengali",
        "Marathi",
        "Gujarati",
        "Tamil",
        "Telugu",
        "Malayalam",
        "Kannada",
        "Punjabi",
    ]

    # dropdown to select destination language
    selected_dest_lang = st.selectbox("Select Destination Language", dest_languages)

    if st.button("Translate"):
        # mapping selected language to language code in googletrans API
        lang_mapping = {
            "Hindi": "hi",
            "English": "en",
            "Bengali": "bn",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "Kannada": "kn",
            "Punjabi": "pa",
        }

        translator = Translator()
        dest_lang_code = lang_mapping.get(selected_dest_lang, "en")
        translated_text = translator.translate(input_text, dest=dest_lang_code)

        st.success("Language Translation Using googletrans API")
        st.info(f"Translated Text ({selected_dest_lang}): {translated_text.text}")


def language_translator():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Language Translator NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        language_translation_techniques(input_text)

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
            language_translation_techniques(text_file)
