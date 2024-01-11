import streamlit as st


def contact_info():
    st.title("Developer Information")

    # Contact information
    contact_html = """
        <style>
            .contact{
                font-size: 22px;
                margin-bottom: 8px;
                margin-top: 10px;
            }
        </style>
        <div class="contact">If you need any assistance, please reach out to us.</div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

    st.write(
        "Email:  [aniket.kumar.giri2707@gmail.com](mailto:aniket.kumar.giri2707@gmail.com)"
    )
    st.write("Phone: [+91 9123997300](tel:+919123997300)")

    # Social media links
    connect_html = """
        <style>
            .connect{
                font-size: 22px;
                margin-top: 28px;
            }
        </style>
        <div class="connect">Connect with us.</div>
    """
    st.markdown(connect_html, unsafe_allow_html=True)

    st.markdown(
        """
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/aniket-giri-b51b281a5/)
        [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter)](https://twitter.com/aniket_giri27)
        [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/anikthe_27/)
        [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github)](https://github.com/aniketkumargiri)
        """,
        unsafe_allow_html=True,
    )
