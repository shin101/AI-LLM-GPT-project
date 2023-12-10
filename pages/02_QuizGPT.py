import streamlit as st
from langchain.retrievers import WikipediaRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader

st.set_page_config(
    page_title="QuizGPT"
)

st.title("QuizGPT")

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-1106"
)

@st.cache_data(show_spinner="Loading file...")
def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs

with st.sidebar:
    docs = None
    choice = st.selectbox("Choose what you want to use", ("File", "Wikipedia Article"))

    if choice == "File":
        file = st.file_uploader("Upload a .docx, .txt or .pdf file", type=["pdf", "txt", "docx"])
        if file: 
            docs = split_file(file)
    else:
        topic = st.text_input("Search Wikipedia")
        if topic:
            retriever = WikipediaRetriever(top_k_results=1)
            with st.status("Searching.."):
                docs = retriever.get_relevant_documents(topic)

if not docs:
    st.markdown(
        """
    Welcome to QuizGPT!
                
    This app will make a quiz from a file you upload or from a Wikipedia article to test your knowledge on a subject. 
                
    Get started by uploading a file or searching on Wikipedia in the sidebar.
    """
    )
else:
    st.write(docs)
