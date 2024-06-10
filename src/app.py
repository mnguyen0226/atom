import os
import streamlit as st
import panel as pn
from database import init_db, insert_ingredients, get_ingredients_by_type
from dotenv import load_dotenv, find_dotenv
import openai

type_to_ingre = {
    "crust": ["thin", "thick", " stuffed", "gluten-free", "cauliflower", "whole wheat"],
    "sauce": ["tomato", "alfredo", "pesto", "barbecue", "garlic", "olive oil"],
    "cheese": [
        "mozzarella",
        "cheddar",
        "parmesan",
        "provolone",
        "feta",
        "blue cheese",
        "ricotta",
        "goat cheese",
        "vegan cheese",
    ],
    "meat": [
        "pepperoni",
        "sausage",
        "bacon",
        "ham",
        "chicken",
        "ground beef",
        "salami",
        "prosciutto",
        "meatballs",
    ],
    "vegetable": [
        "mushrooms",
        "onions",
        "bell peppers",
        "black olives",
        "spinach",
        "artichokes",
        "tomatoes",
        "jalapeño",
        "pineapple",
        "garlic",
        "broccoli",
        "arugula",
    ],
    "additional": [
        "fresh basil",
        "oregano",
        "red pepper flakes",
        "balsamic",
        "glaze",
        "sun-dried tomatoes",
        "capers",
        "anchovies",
        "avocado",
    ],
    "seasoning": [
        "italian herbs",
        "crushed red pepper",
        "garlic powder",
        "onion powder",
        "freshly grounded black pepper",
    ],
}

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


# Create ingredients to database
init_db()

# # Insert ingredients to database
# insert_ingredients(type_to_ingre)

# # Try to get all the values of each table
# for item in type_to_ingre.keys():
#     print(get_ingredients_by_type(item))

st.title("Pizza Order Management System")

tab1, tab2 = st.tabs(["Client Bot", "Order Bot"])


with tab1:
    st.header("Build Your Pizza")

    context = [
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

    input_text = st.text_input("Enter your message here...", "Hi")
    if st.button("Send"):
        context.append({"role": "user", "content": input_text})
        response = get_completion_from_messages(context)
        context.append({"role": "assistant", "content": response})

        for message in context:
            st.write(f"{message['role'].capitalize()}: {message['content']}")

with tab2:
    st.header("Clients' Orders")
