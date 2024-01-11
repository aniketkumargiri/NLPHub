import streamlit as st
import docx2txt
import pdfplumber
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")


# plotting word length distribution
def plot_mendenhall_curve(docx):
    word_length = [len(token) for token in docx.split()]
    word_length_counts = Counter(word_length)
    sorted_word_length_counts = sorted(dict(word_length_counts).items())

    x, y = zip(*sorted_word_length_counts)
    fig = plt.figure(figsize=(20, 10))
    plt.plot(x, y, color="hotpink")
    plt.title("Plot of Word Length Distribution(Mendenhall Curve)")
    plt.show()
    st.pyplot(fig)


def display_topic_modeling(text):
    if st.button("Display"):
        st.success("Stylometry Curve Plot")
        plot_mendenhall_curve(text)


def topic_modeling():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Topic Modeling NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        display_topic_modeling(input_text)

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
            display_topic_modeling(text_file)
