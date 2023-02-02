import streamlit as st

from assistance._keys import get_openai_api_key


def get_openai_key_via_streamlit_session():
    if "openai_key" in st.session_state:
        return st.session_state.openai_key

    try:
        key = get_openai_api_key()

    except FileNotFoundError:
        if "openai_key" not in st.session_state:
            st.write("OpenAI API key not found.")

            key = st.text_input(
                "Enter your OpenAI API key (will only be temporarily stored within this server instance):"
            )
            if not key:
                st.stop()

    st.session_state.openai_key = key

    return key
