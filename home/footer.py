import streamlit as st


def footer():
    footer_html = """
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                text-align: center;
                padding: 10px;
                color: #62098f;
            }
        </style>
        <div class="footer">Made with ❤️ by Aniket Giri</div>
    """
    # Footer
    st.markdown(footer_html, unsafe_allow_html=True)
