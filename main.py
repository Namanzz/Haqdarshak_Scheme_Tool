# Import necessary libraries
import streamlit as st  # Streamlit for building the web app
from utils.loader import load_and_process_urls  # Function to load and process scheme URLs
from utils.qa_engine import initialize_qa, ask_question  # Functions for question answering
from utils.summarizer import generate_summary  # Function to generate summaries
import os  # OS module for environment variables
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from .env file
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="Haqdarshak Scheme Research Tool")
st.title("🧠 Government Scheme Research Assistant")
st.write("This tool helps summarize government schemes and lets you ask questions based on their content.")

# Sidebar for user to input scheme URLs
st.sidebar.header("🔗 Input Scheme URLs")
url_text = st.sidebar.text_area("Enter URLs (one per line):")
process_button = st.sidebar.button("🚀 Process URLs")

# Initialize session state variables if not already present
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'faiss_index' not in st.session_state:
    st.session_state.faiss_index = None
if 'summaries' not in st.session_state:
    st.session_state.summaries = {}

# Process URLs when the user clicks the button
if process_button:
    with st.spinner("Processing URLs..."):
        # Load documents, generate summaries, and create FAISS index
        docs, summaries, faiss_index = load_and_process_urls(url_text.strip().split("\n"))
        st.session_state.documents = docs
        st.session_state.faiss_index = faiss_index
        st.session_state.summaries = summaries
    st.success("✅ URLs processed and indexed!")

# Display summaries if available
if st.session_state.summaries:
    st.subheader("📄 Scheme Summaries")
    for url, summary in st.session_state.summaries.items():
        st.markdown(f"**URL**: {url}")
        st.markdown(f"**Summary**:\n{summary}")
        st.markdown("---")

# Section for user to ask questions about the schemes
st.subheader("❓ Ask Questions About the Schemes")
user_query = st.text_input("Type your question and hit Enter...")

if user_query:
    if st.session_state.faiss_index is None:
        st.warning("Please process URLs first.")
    else:
        with st.spinner("Thinking..."):
            # Get answer and source URL for the user's question
            answer, source_url = ask_question(
                user_query, st.session_state.faiss_index, st.session_state.documents
            )
            st.markdown("### ✅ Answer")
            st.write(answer)
            if source_url:
                st.markdown(f"**From URL:** {source_url}")
                if source_url in st.session_state.summaries:
                    st.markdown("**Summary**:")
                    st.write(st.session_state.summaries[source_url])
        st.success("Your question has been answered!")