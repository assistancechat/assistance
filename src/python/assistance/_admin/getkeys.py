import openai
import streamlit as st

from assistance._keys import set_openai_api_key


def check_and_set_open_ai_key():
    try:
        set_openai_api_key()
        return

    except FileNotFoundError:
        if "openai_key" not in st.session_state:
            st.write("OpenAI API key not found.")

            key = st.text_input(
                "Enter your OpenAI API key (will only be temporarily stored within this server instance):"
            )
            if not key:
                st.stop()

            st.session_state.openai_key = key

        openai.api_key = st.session_state.openai_key
