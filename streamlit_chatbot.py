import streamlit as st
import openai

st.title(" chatbot with OpenAI GPT")
st.caption("컴퓨터소프트웨어학부 23115408 허재우")

with st.sidebar:
    st.markdown("[GPT an OpenAI API key](https://platform.openai.com/api-keys)")

client = OpenAI(api_key=st.secerets("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.message.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for reponse in client.chat.completions.create(
            model=st.session_state["openai_model"],
            message=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (reponse.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
    st.session_state.message.append({"role": "assistant", "content": full_response})