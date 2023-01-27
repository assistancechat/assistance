from assistance._admin import categories

CATEGORY = categories.AI_CREATIONS
TITLE = "A GPT Chat"


import openai
import streamlit as st


def main():
    st.title("A GPT Chat")
    st.write("Talk to an AI assistant using GPT-3")

    user_input = st.text_input("Enter your message here:")

    if user_input:
        # Use openAI engine text-davinci-003
        response = openai.Completion.create(
            engine="davinci-003",
            prompt=user_input,
            temperature=0.7,
            max_tokens=50,
        )
        st.write("AI Assistant: ", response["choices"][0]["text"])


if __name__ == "__main__":
    main()
