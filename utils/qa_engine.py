"""
This module provides utilities for question answering using a HuggingFace pipeline and FAISS vector store.
Functions:
    initialize_qa():
        Initializes a HuggingFace text2text-generation pipeline with the "google/flan-t5-base" model,
        wraps it in a LangChain HuggingFacePipeline, and returns the LLM object.
    ask_question(query: str, faiss_index: FAISS, documents: List[Document]) -> Tuple[str, str]:
        Given a user query, a FAISS vector index, and a list of documents, retrieves the top 3 most relevant documents
        using similarity search. Extracts the source URL from the most relevant document's metadata (if available).
        Initializes the QA pipeline and runs a question-answering chain using the retrieved documents and the query.
        Returns a tuple containing the generated answer and the source URL. Handles exceptions and returns an error message if any occur.
"""
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from typing import Tuple, List

def initialize_qa():
    qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=512)
    llm = HuggingFacePipeline(pipeline=qa_pipeline)
    return llm

# Main function to ask questions using FAISS
def ask_question(query: str, faiss_index: FAISS, documents: List[Document]) -> Tuple[str, str]:
    try:
        retriever = faiss_index.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        relevant_docs = retriever.get_relevant_documents(query)

        source_url = ""
        if relevant_docs:
            source_url = relevant_docs[0].metadata.get("source", "")

        llm = initialize_qa()
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=relevant_docs, question=query)

        return answer, source_url

    except Exception as e:
        return f"Error during Q&A: {e}", ""
