import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

st.set_page_config(page_title="Langchain: Summarise Text from Yt or Website")
st.title("Langchain: Summarise Text from YT or website")
st.subheader("Summarise URL")

## Get the Groq API Key and url (YT or website) to be summarised
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")
llm = ChatGroq(model="Llama3-8b-8192", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""

prompt=PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarise the content from YT or website"):

    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information")

    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can may be a YT video url or website url")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the websitre or yt video data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                 header={"User-Agent": "Mozilla/5.0 (Machintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs = loader.load()

                chain=load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)

        except Exception as e:

            st.exception(f"Exception: {e}")

