from assistance._admin import categories

CATEGORY = categories.DEMO
TITLE = "Student Assistance Chat"


import openai
import streamlit as st


def main():
    user_input = st.text_input("Enter your message here:")

    if user_input:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            temperature=0.7,
            max_tokens=50,
        )
        st.write("AI Assistant: ", response["choices"][0]["text"])
