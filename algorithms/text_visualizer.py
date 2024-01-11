import streamlit as st
import docx2txt
import pdfplumber
from collections import Counter
import neattext.functions as nfx
import neattext as nt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")


def text_description(text):
    word_desc = nt.TextFrame(text).word_stats()
    st.write(word_desc)


def get_most_common_tokens(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    st.write(dict(most_common_tokens))

    x, y = zip(*most_common_tokens)
    fig = plt.figure(figsize=(20, 10))
    plt.bar(x, y, color="indigo")
    plt.title("Plot of Most Common Tokens")
    plt.show()
    st.pyplot(fig)


def plot_wordcloud(docx):
    mywordcloud = WordCloud(background_color="white").generate(docx)
    plt.title("Word Cloud Visualization")
    plt.imshow(mywordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()


def show_text_visualization(text):
    if st.button("Visualize"):
        st.success("Text Description")
        text_description(text)

        st.info("Most Common Tokens")
        processed_text = nfx.remove_stopwords(text)
        get_most_common_tokens(processed_text)

        st.error("Word Cloud Visualization")
        plot_wordcloud(text)


def text_visualizer():
    # Subheader
    st.markdown(
        "<h2 style='color: purple;'>Text Visualizer NLP APP</h2><br>",
        unsafe_allow_html=True,
    )

    input_menu = ["Enter Text", "Drop Files"]
    choice = st.sidebar.selectbox("Input Text Format", input_menu)

    if choice == "Enter Text":
        input_text = st.text_area("Enter your text here...", key="input_text")
        show_text_visualization(input_text)

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
            show_text_visualization(text_file)
