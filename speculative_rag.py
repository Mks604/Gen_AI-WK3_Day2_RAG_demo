import os

# Required for FAISS
import numpy as np
import faiss

# Correct imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import PromptTemplate

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# --- Step 1: Build the knowledge base --- #
texts = [
    "Python was created by Guido van Rossum.",
    "LangChain helps glue LLMs and apps together.",
    "FAISS is a vector database for efficient similarity search.",
    "Speculative RAG tries to answer even when exact info is missing."
]

# Create embeddings
embeddings = OpenAIEmbeddings()

# Use from_texts() to build the vectorstore
vectorstore = FAISS.from_texts(
    texts=texts,
    embedding=embeddings
)

# --- Step 2: Prepare the prompt --- #
speculative_prompt = PromptTemplate.from_template(
    """
You are a speculative assistant. Use the context below to answer the question.
If unsure, make a reasoned guess and explicitly label it as speculative.

Context:
{context}

Question:
{question}

Answer:
"""
)

# --- Step 3: Create the LLM --- #
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# --- Step 4: Speculative RAG function --- #
def speculative_rag(question, top_k=2):
    # Retrieve similar docs
    docs = vectorstore.similarity_search(question, k=top_k)
    context = "\n".join([doc.page_content for doc in docs])  # join text only

    # Create prompt text
    prompt_text = speculative_prompt.format(
        context=context, question=question
    )

    # Call the LLM
    result = llm.invoke(prompt_text)
    return result.content

# --- Step 5: Test --- #
print("Answer 1:", speculative_rag("Who founded LangChain?"))
print("Answer 2:", speculative_rag("Can Python be used for quantum computing?"))