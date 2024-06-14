import openai
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("roles/orderbot.txt", "r") as file:
    role_content = file.read()

context_dict = {
    "role": "system",
    "content": role_content,
}

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [context_dict]

# Add title and markdown to the sidebar
st.sidebar.title("A.T.O.M")
st.sidebar.markdown("International student assistant in the U.S.")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Enter your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=0,
        )
        assistant_reply = response.choices[0].message["content"]
        st.markdown(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
