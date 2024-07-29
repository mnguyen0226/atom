import openai
import streamlit as st
import os
from dotenv import load_dotenv
from dotenv import find_dotenv

from utils import reset_conversation
from utils import get_completion_from_messages
from utils import find_category_and_product_only
from utils import get_products_and_category
from utils import read_string_to_list
from utils import generate_output_string


# Get local open ai token
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

DELIMITER = "```"


def main():
    context_dict = {"role": "system", "content": "You are a Service Assistant"}

    # Initialize the state for model and messages (role, content) storage
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state["messages"] = [context_dict]

    # Streamlit
    st.set_page_config(
        page_title="Service Assistant", page_icon=":rocket:", layout="wide"
    )
    st.logo(
        image="images/amazon_logo.png",
        icon_image="images/amazon_logo.png",
    )
    st.sidebar.title("Service Assistant")
    st.sidebar.markdown("Provide customer service")
    if st.sidebar.button("Reset Conversation", use_container_width=True):
        reset_conversation(context_dict)
        st.rerun()

    # Display all messages
    for message in st.session_state["messages"]:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User prompt and answer from the chatbot
    if user_input := st.chat_input("Enter your message here..."):
        # Add the (user-content) into session state
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        assistant_reply = ""

        with st.chat_message("assistant"):
            # Moderate the user input
            response = openai.Moderation.create(input=user_input)
            moderation_output = response["results"][0]
            if moderation_output["flagged"]:
                st.sidebar.warning("Input flagged by Moderation API")
                assistant_reply = "Sorry, we cannot process this request."
            else:
                category_and_product_response = find_category_and_product_only(
                    user_input, get_products_and_category()
                )
                print(category_and_product_response)

                # Extract the llist of product
                category_and_product_list = read_string_to_list(
                    category_and_product_response
                )
                print(category_and_product_list)

                # If products are found, look them up
                product_information = generate_output_string(category_and_product_list)

                # Answer the user questions
                system_message = f"""
                    You are a customer service assistant for a large electronic store. \
                    Respond in a friendly and helpful tone, with concise answers. \
                    Make sure to ask the user relevant follow-up questions.
                """

                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{DELIMITER}{user_input}{DELIMITER}"},
                    {
                        "role": "assistant",
                        "content": f"Relevant product information:\n{product_information}",
                    },
                ]

                final_response = get_completion_from_messages(
                    st.session_state["messages"] + messages
                )

                # Put the answerthru moderation api
                response = openai.Moderation.create(input=final_response)
                moderation_output = response["results"][0]
                if moderation_output["flagged"]:
                    st.sidebar.warning("Response flagged by Moderation API")
                    assistant_reply = "Sorry, we cannot provide this request."

                # Ask the model if the response answered the initial user query well
                user_message = f"""
                Customer message: {DELIMITER}{user_input}{DELIMITER}
                Agent response: {DELIMITER}{final_response}{DELIMITER}

                Does the response sufficiently answer the question?
                """
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ]
                evaluation_response = get_completion_from_messages(messages)

                # If yes, use the answer, if not, say that you will conect the user to a human
                if "Y" in evaluation_response:
                    assistant_reply = final_response
                else:
                    st.sidebar.warning("Response flagged by Moderation API")
                    assistant_reply = "I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."

            st.markdown(assistant_reply)

        # Add the response to the session state
        st.session_state["messages"].append(
            {"role": "assistant", "content": assistant_reply}
        )


if __name__ == "__main__":
    main()
