from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
import streamlit as st

html2text_transformer = Html2TextTransformer()

st.markdown(
    """
    # SiteGPT
            
    Ask any questions about the content of a website.
    Start by writing the URL of the website on the sidebar.
"""
)

with st.sidebar:
    url = st.text_input("Search by URL", placeholder="http://...")

if url:
    # async chromium loader to scrape the website 
    loader = AsyncChromiumLoader([url])
    docs = loader.load()
    transformed = html2text_transformer.transform_documents(docs)
    st.write(docs)