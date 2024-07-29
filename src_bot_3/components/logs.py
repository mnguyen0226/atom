import streamlit as st


def log_page():
    st.title("Answer Logs")

    if "feedback" in st.session_state:
        for i, feedback in st.session_state["feedback"].items():
            if feedback["thumbs_up"] != 0 and feedback["thumbs_down"] != 0:
                st.markdown(f"**User Prompt:** {feedback['user_prompt']}")
                st.markdown(f"**Assistant Reply:** {feedback['assistant_reply']}")
                st.markdown(f"**Thumbs Up Count:** {feedback['thumbs_up']}")
                st.markdown(f"**Thumbs Down Count:** {feedback['thumbs_down']}")
                st.markdown("---")
