import streamlit as st
from home import header, contents, footer
from algorithms import applications
from documentation import developer


def main():
    st.set_page_config(page_title="NLPAlgoHub", page_icon="images/favicon.ico")

    menu = ["Home", "Applications", "Developer"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        header.header()
        contents.contents()
        footer.footer()

    elif choice == "Applications":
        applications.algos()

    elif choice == "Developer":
        developer.contact_info()


if __name__ == "__main__":
    main()
