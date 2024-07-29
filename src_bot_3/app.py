import streamlit as st
from components.services import service_page
from components.logs import log_page


def main():
    st.set_page_config(
        page_title="Service Assistant", page_icon=":rocket:", layout="wide"
    )
    st.logo(
        image="images/amazon_logo.png",
        icon_image="images/amazon_logo.png",
    )
    st.sidebar.title("Navigation")
    page_names_to_func = {"Customer Service": service_page, "Logs": log_page}

    demo_name = st.sidebar.selectbox("", page_names_to_func.keys())
    page_names_to_func[demo_name]()


if __name__ == "__main__":
    main()
