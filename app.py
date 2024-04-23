import streamlit as st
from unify import Unify


def input_fields():
    with st.sidebar:
        st.session_state.unify_key = st.text_input("UNIFY KEY", type="password")
        st.session_state.llm_1 = st.selectbox(
            "Select LLM 1",
            ["mistral-7b-instruct-v0.1@deepinfra"]  # we can add more models
        )
        st.session_state.llm_2 = st.selectbox(
            "Select LLM 2",
            ["llama-2-13b-chat@anyscale"]  # same
        )


def chat_interface(prompt, llm1_endpoint, llm2_endpoint, unify_key):
    agent1 = Unify(
        api_key=unify_key,
        endpoint=llm1_endpoint
    )
    agent2 = Unify(
        api_key=unify_key,
        endpoint=llm2_endpoint
    )
    response1 = agent1.generate(user_prompt=prompt, stream=True)
    response2 = agent2.generate(user_prompt=prompt, stream=True)

    st.write("Output from LLM 1:")
    st.write_stream(response1)

    st.write("Output from LLM 2:")
    st.write_stream(response2)


def main():
    st.set_page_config(page_title="Dual LLM Chat Interface")
    st.title("Dual LLM Chat Interface")

    input_fields()

    prompt = st.text_input("Enter your prompt here:")

    if prompt:
        chat_interface(prompt, st.session_state.llm_1, st.session_state.llm_2, st.session_state.unify_key)


if __name__ == "__main__":
    main()
