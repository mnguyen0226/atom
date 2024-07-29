# ATOM

`Customed chatbot based on prompted roles with Python, Streamlit, SQLite, and ChatGPT API.`
- Chatbot 1: Generic by single prompt.
- Chatbot 2: Customer services with chain of thoughts.
- Chatbot 3: Allow for user to thumbs up and down
- TODO:
  - Disable like / not like when generate.
  - One question at a time.
  - Need to extract data with LLMs
  - Log feedbacks in database (Feedbacks)
  - Authentication for single user per feedbacks
  - How to allow manager to insert data (Azure Intelligence Docs? or Forms?)

### Applications
- Use to train/assist multiple people with a small amount of documentation.

### Ideas
- Create a form to submit "context", then store in database so that the bot has more information.
- Maybe create a customed form of attributes. Store in database.

### Reproduction
```python
conda create -n atom python=3.8
conda activate atom
pip install -r requirements.txt
cd src
streamlit run app.py
```

### References
[1] [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

[2] [Building Systems with ChatGPT](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)
