import streamlit as st
from unify import Unify

st.set_page_config(page_title="Debate App built with Unify")


def input_fields():
    with st.sidebar:
        st.session_state.unify_key = st.text_input("UNIFY KEY", type="password")
        st.image("robot_icon_green.png", width=20)
        st.session_state.llm_1 = st.selectbox(
            "Select LLM to debate supporting the topic",
            ["mistral-7b-instruct-v0.1@deepinfra", "gpt-4@deepinfra", "codellama-7b-instruct@octoai",
             "gpt-3.5-turbo@openai", "pplx-70b-chat@perplexity-ai","llama-3-8b-chat@together-ai"]

        )
        st.image("robot_icon_yellow.png", width=20)
        st.session_state.llm_2 = st.selectbox(
            "Select LLM to debate opposing the topic",
            ["llama-2-13b-chat@anyscale", "gemma-2b-it@together-ai", "gpt-4-turbo@openai",
             "deepseek-coder-33b-instruct@together-ai", "mistral-large@mistral-ai","llama-3-8b-chat@fireworks-ai"]  # same
        )
        st.session_state.exchange = st.number_input("number of exchanges", min_value=1, max_value=5)


def initialize_model(llm_endpoint, unify_key):
    model = Unify(
        api_key=unify_key,
        endpoint=llm_endpoint
    )
    return model


# Function to generate response from a model given a prompt
def generate_response(model, topic, position, prompt):
    messages = [
        {"role": "system", "content": f"You are debating {position} the following topic: {topic}, "
                                      f"consider the opposing points and provide a response."},
    ]
    messages.extend(prompt)
    return model.generate(messages=messages, stream=True)


def main():
    st.title("Debate App built with Unify")
    st.text("Choose two LLMs to debate each other on a given topic.")

    input_fields()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    topic = st.text_input("Enter the debate topic here:")

    model1 = initialize_model(st.session_state.llm_1, st.session_state.unify_key)
    model2 = initialize_model(st.session_state.llm_2, st.session_state.unify_key)

    if topic:
        model1_messages = []
        model2_messages = []
        for _i in range(st.session_state.exchange):
            with st.chat_message(name="model1", avatar="robot_icon_green.png"):
                if len(model1_messages) == 0:
                    stream = generate_response(model1, topic, "for", [{"role": "user", "content": "start debate."}])
                else:
                    model1_messages.append({"role": "user", "content": model2_response})
                    stream = generate_response(model1, topic, "for", model1_messages)
                model1_response = st.write_stream(stream)
            model1_messages.append({"role": "assistant", "content": model1_response})

            with st.chat_message(name="model2", avatar="robot_icon_yellow.png"):
                model2_messages.append({"role": "user", "content": model1_response})
                stream = generate_response(model2, topic, "against", model2_messages)
                model2_response = st.write_stream(stream)
            model2_messages.append({"role": "assistant", "content": model2_response})


if __name__ == "__main__":
    main()
