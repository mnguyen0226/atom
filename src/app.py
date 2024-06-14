import openai
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

role = "blackstone_or"
# role = "tech_mock"
# role = "harvard_advisor"
# role = "orderbot"

with open(f"roles/{role}.txt", "r") as file:
    role_content = file.read()

context_dict = {
    "role": "system",
    "content": role_content,
}

# Initialize session state if not already initialized
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [context_dict]

# Add title and markdown to the sidebar
st.sidebar.title("A.T.O.M")
st.sidebar.markdown("Role-based assistant via prompting.")


# Function to reset the conversation
def reset_conversation():
    st.session_state.messages = [context_dict]
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# Display reset button in the sidebar
if st.sidebar.button("Reset Conversation"):
    reset_conversation()

# Display messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input and assistant response logic
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
            temperature=0.3,
        )
        assistant_reply = response.choices[0].message["content"]
        st.markdown(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
