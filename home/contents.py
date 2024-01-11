import streamlit as st


def contents():
    # list of NLP tasks
    nlp_tasks = [
        "Word Representation",
        "Word Embedding",
        "Part of Speech Tagging",
        "Named Entity Recognition",
        "Dependency Parsing",
        "Topic Modeling",
        "Keyword Extraction",
        "Text Visualization",
        "Text Analysis",
        "Text Summarization",
        "Language Translation",
    ]

    # ordered list of NLP tasks
    ordered_nlp_tasks = "\n".join(
        [f"1. <span style='color: blue;'>{task}</span>" for task in nlp_tasks]
    )

    # displaying the tasks performed by the application
    st.markdown(ordered_nlp_tasks, unsafe_allow_html=True)
