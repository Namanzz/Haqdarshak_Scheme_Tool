"""
This module provides utilities for loading, processing, and summarizing PDF documents from given URLs,
splitting them into manageable text chunks, generating summaries, and creating a FAISS vector store for embeddings.
Functions:
    load_and_process_urls(urls: List[str]) -> Tuple[List, Dict[str, str], FAISS]:
        Downloads PDF files from the provided list of URLs, extracts their content, splits the content into chunks,
        generates summaries for each document, computes embeddings, and stores them in a FAISS vector store.
        Args:
            urls (List[str]): A list of URLs pointing to PDF files to be processed.
        Returns:
            Tuple[List, Dict[str, str], FAISS]:
                - List of split document chunks.
                - Dictionary mapping each URL to its generated summary.
                - FAISS vector store containing the embeddings of the document chunks.
        Raises:
            ValueError: If no documents could be loaded from the provided URLs.
        Side Effects:
            - Downloads and temporarily stores PDF files.
            - Writes the FAISS vector store to a pickle file named 'faiss_store_openai.pkl'.
"""
import os
import pickle
import tempfile
import requests
from typing import List, Tuple, Dict

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from utils.summarizer import generate_summary


def load_and_process_urls(urls: List[str]) -> Tuple[List, Dict[str, str], FAISS]:
    documents = []
    summaries = {}
    all_docs = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to download: {url}")
                continue

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name

            loader = PyMuPDFLoader(tmp_file_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = url  # manually attach URL as source
            all_docs.extend(docs)

            os.remove(tmp_file_path)  # clean up

        except Exception as e:
            print(f"Error processing {url}: {e}")

    if not all_docs:
        raise ValueError("No documents were loaded. Please check the URLs.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(all_docs)

    for doc in all_docs:
        url = doc.metadata.get("source", "")
        summaries[url] = generate_summary(doc.page_content)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_documents(texts, embeddings)

    with open("faiss_store_openai.pkl", "wb") as f:
        pickle.dump(faiss_index, f)

    return texts, summaries, faiss_index