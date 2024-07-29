import streamlit as st
import openai
import json
import collections

PRODUCTS_FILE = "data/products.json"
CATEGORIES_FILE = "data/categories.json"


def reset_conversation(context_dict):
    """Reset conversation"""
    st.session_state["messages"] = [context_dict]
    st.session_state["openai_model"] = "gpt-3.5-turbo"


def get_completion_from_messages(
    messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500
):
    """Generate response based on the input message"""
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]


def get_products():
    """Get the json of all products details"""
    with open(PRODUCTS_FILE, "r") as file:
        products = json.load(file)
    return products


def get_products_and_category():
    """Get a dict of category to products details"""
    products = get_products()
    products_by_category = collections.defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get("category")
        if category:
            products_by_category[category].append(product_info.get("name"))

    return dict(products_by_category)


def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with \
    {delimiter} characters.
    Output a python list of objects, where each object has \
    the following format:
        'category': <one of Computers and Laptops, \
        Smartphones and Accessories, \
        Televisions and Home Theater Systems, \
        Gaming Consoles and Accessories, 
        Audio Equipment, Cameras and Camcorders>,
    OR
        'products': <a list of products that must \
        be found in the allowed products below>

    Where the categories and products must be found in \
    the customer service query.
    If a product is mentioned, it must be associated with \
    the correct category in the allowed products list below.
    If no products or categories are found, output an \
    empty list.
    If a category is mentioned, then provide the list of products.

    Allowed products: 

    Computers and Laptops category:
    TechPro Ultrabook
    BlueWave Gaming Laptop
    PowerLite Convertible
    TechPro Desktop
    BlueWave Chromebook

    Smartphones and Accessories category:
    SmartX ProPhone
    MobiTech PowerCase
    SmartX MiniPhone
    MobiTech Wireless Charger
    SmartX EarBuds

    Televisions and Home Theater Systems category:
    CineView 4K TV
    SoundMax Home Theater
    CineView 8K TV
    SoundMax Soundbar
    CineView OLED TV

    Gaming Consoles and Accessories category:
    GameSphere X
    ProGamer Controller
    GameSphere Y
    ProGamer Racing Wheel
    GameSphere VR Headset

    Audio Equipment category:
    AudioPhonic Noise-Canceling Headphones
    WaveSound Bluetooth Speaker
    AudioPhonic True Wireless Earbuds
    WaveSound Soundbar
    AudioPhonic Turntable

    Cameras and Camcorders category:
    FotoSnap DSLR Camera
    ActionCam 4K
    FotoSnap Mirrorless Camera
    ZoomMaster Camcorder
    FotoSnap Instant Camera

    Only output the list of objects, with nothing else.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
    ]
    return get_completion_from_messages(messages)


def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        # Ensure the input is a string
        if isinstance(input_string, list):
            input_string = str(input_string)

        input_string = input_string.replace(
            "'", '"'
        )  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None


# product look up (either by category or by product within category)
def get_product_by_name(name):
    products = get_products()
    return products.get(name, None)


def get_products_by_category(category):
    products = get_products()
    return [product for product in products.values() if product["category"] == category]


def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string
