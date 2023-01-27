import streamlit as st

from assistance._keys import get_openai_api_key, write_openai_api_key


def check_and_get_open_ai_key():
    try:
        key = get_openai_api_key()
    except FileNotFoundError:
        st.write("OpenAI API key not found.")

        key = st.text_input("Enter your OpenAI API key:")
        if not key:
            st.stop()

        write_openai_api_key(key)

    return key
