import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import openai

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to get completion from a single prompt
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # degree of randomness in the model's output
    )
    return response.choices[0].message["content"]


# Function to get completion from a list of messages
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # degree of randomness in the model's output
    )
    return response.choices[0].message["content"]


# Initialize context in session state
if "context" not in st.session_state:
    st.session_state.context = [
        {
            "role": "system",
            "content": """
            You are OrderBot, an automated service to collect orders for a pizza restaurant. \
            You first greet the customer, then collect the order, \
            and then ask if it's a pickup or delivery. \
            You wait to collect the entire order, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            If it's a delivery, you ask for an address. \
            Finally, you collect the payment.\
            Make sure to clarify all options, extras, and sizes to uniquely \
            identify the item from the menu.\
            You respond in a short, very conversational friendly style. \
            The menu includes \
            pepperoni pizza  12.95, 10.00, 7.00 \
            cheese pizza   10.95, 9.25, 6.50 \
            eggplant pizza   11.95, 9.75, 6.75 \
            fries 4.50, 3.50 \
            greek salad 7.25 \
            Toppings: \
            extra cheese 2.00, \
            mushrooms 1.50 \
            sausage 3.00 \
            canadian bacon 3.50 \|
            AI sauce 1.50 \
            peppers 1.00 \
            Drinks: \
            coke 3.00, 2.00, 1.00 \
            sprite 3.00, 2.00, 1.00 \
            bottled water 5.00 \
            """,
        }
    ]

st.title("A.T.O.M")
st.subheader("Chatbot for college student questions")

# Input section
input_text = st.text_input("Enter your message here...", "Hi")
if st.button("Send"):
    st.session_state.context.append({"role": "user", "content": input_text})
    response = get_completion_from_messages(st.session_state.context)
    st.session_state.context.append({"role": "assistant", "content": response})

# Display conversation history
for message in st.session_state.context:
    st.write(f"{message['role'].capitalize()}: {message['content']}")
