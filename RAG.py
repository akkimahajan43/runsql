import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from groq import Groq
import tempfile
from dotenv import load_dotenv
import os

# -----------------------------
# GROQ API KEY
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# -----------------------------
# CUSTOM EMBEDDINGS CLASS
# -----------------------------
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="PDF Chatbot", page_icon="🤖")

st.title("🤖 PDF Chatbot")

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# -----------------------------
# PROCESS PDF ONLY ONCE
# -----------------------------
if uploaded_file and st.session_state.vectorstore is None:

    with st.spinner("Processing PDF..."):

        # Save temporary PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = text_splitter.split_documents(documents)

        # Embeddings
        embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # Create Vector DB
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Store in session
        st.session_state.vectorstore = vectorstore

    st.success("PDF processed successfully!")

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
if st.session_state.vectorstore:

    user_question = st.chat_input("Ask something from the PDF")

    if user_question:

        # Show user message
        st.chat_message("user").markdown(user_question)

        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        # Similarity search
        relevant_docs = st.session_state.vectorstore.similarity_search(
            user_question,
            k=3
        )

        context = "\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        prompt = f"""
        Answer the question ONLY from the provided PDF context.

        Context:
        {context}

        Question:
        {user_question}
        """

        # LLM Response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        # Show assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Store assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })