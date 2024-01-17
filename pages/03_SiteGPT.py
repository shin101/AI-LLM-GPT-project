from langchain.document_loaders import SitemapLoader
import streamlit as st

@st.cache_data(show_spinner = "Loading website..")
def load_website(url):
	loader = SitemapLoader(url)
	# make loading slow to prevent being blocked by the website
	loader.requests_per_second = 1
	docs = loader.load()
	return docs

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
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        docs = load_website(url)
