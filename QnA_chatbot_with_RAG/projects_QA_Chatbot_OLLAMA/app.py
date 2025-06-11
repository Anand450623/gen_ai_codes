from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot with Ollama"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You're a helpful assistant. Please response to the user queries"),
        ("user", "Question :{question}")
    ]
)


def generate_response(question, engine, tempreture, max_token):

    llm = Ollama(model=engine)
    output_parser=StrOutputParser()
    chain = prompt|llm|output_parser
    answer=chain.invoke({'question': question})
    return answer


## Title of the app
st.title("Simple Q&A Chatbot with Ollama")

## Sidebar for settings
st.sidebar.title("Settings")

## Drop down to select various OpenAI models
engine=st.sidebar.selectbox("Select an Open AI Model", ["gemma2:latest", "llama3.2:latest", "gemma:2b", "mxbai-embed-large:latest", "llama3.1:8b"])

## Adjust reponse parameter
temperature = st.sidebar.slider("Tempreture", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Token", min_value=50, max_value=300, value=150)

## Main interface for user input
st.write("Go ahead and ask your question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, engine, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")
