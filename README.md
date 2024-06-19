# ATOM

`Customed chatbot based on prompted roles with Python, Streamlit, SQLite, and ChatGPT API.`

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
