# src/core/rag_pipeline.py
"""
Core RAG (Retrieval-Augmented Generation) Pipeline.

This module contains the RAGPipeline class, which orchestrates the entire
process of answering a user's question based on a knowledge base. It uses the
LangChain Expression Language (LCEL) to build a declarative and efficient chain.
"""

from typing import List, Dict, Any
from operator import itemgetter

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore

# This constant defines the prompt template for the RAG chain.
# It instructs the LLM on how to behave, how to use the provided context,
# what to do if the answer isn't found, and in which language to respond.
RAG_PROMPT_TEMPLATE = """
As a helpful informational assistant, your task is to answer the user's question
based exclusively on the provided context. Be concise and factual.

If the context does not contain the answer, you must reply with:
"Unfortunately, I could not find information on this topic in my knowledge base."

Your final answer must be in the following language: {language}

Context:
{context}

Question:
{question}
"""


class RAGPipeline:
    """
    Orchestrates the retrieval-augmented generation process.

    This class encapsulates the logic for taking a user question, retrieving
    relevant context from a vector store, and generating a response using an LLM.
    """

    def __init__(self, llm: Runnable, vector_store: VectorStore, top_k: int = 5):
        """
        Initializes the RAG pipeline by constructing the LCEL chain.

        Args:
            llm (Runnable): The language model to be used for generation.
            vector_store (VectorStore): The vector store for document retrieval.
            top_k (int): The number of relevant documents to retrieve.
        """
        self.llm = llm
        self.vector_store = vector_store
        self.retriever: BaseRetriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

        # Define the retrieval sub-chain. It takes a dictionary as input,
        # extracts the 'question', passes it to the retriever,
        # and formats the resulting documents into a single context string.
        retrieval_chain = (
            itemgetter("question")
            | self.retriever
            | self._format_context
        )

        # Define the main RAG chain using LCEL.
        # This chain expects an input dictionary: {"question": str, "language": str}
        self.chain = (
            RunnableParallel(
                # The 'context' key is populated by the retrieval_chain.
                context=retrieval_chain,
                # 'question' and 'language' keys are passed through directly
                # from the input dictionary.
                question=RunnablePassthrough(),
                language=RunnablePassthrough()
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    @staticmethod
    def _format_context(docs: List[Document]) -> str:
        """
        Formats a list of retrieved documents into a single string context.

        Args:
            docs (List[Document]): The list of documents from the retriever.

        Returns:
            str: A formatted string containing the content of all documents.
        """
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def _format_sources(docs: List[Document]) -> List[Dict[str, str]]:
        """
        Extracts unique source information from a list of documents.

        Args:
            docs (List[Document]): The list of documents from the retriever.

        Returns:
            List[Dict[str, str]]: A list of unique sources, each with a URL and title.
        """
        sources = []
        unique_urls = set()
        for doc in docs:
            source_url = doc.metadata.get("source")
            if source_url and source_url not in unique_urls:
                sources.append({
                    "url": source_url,
                    "title": doc.metadata.get("title", "No Title")
                })
                unique_urls.add(source_url)
        return sources

    def answer(self, question: str, language: str = "Polish") -> Dict[str, Any]:
        """
        Executes the full RAG process for a given question in a specified language.

        Args:
            question (str): The user's question.
            language (str): The language for the generated answer (e.g., "Polish", "English").

        Returns:
            Dict[str, Any]: A dictionary containing the generated 'answer' and
                            a list of 'sources'.
        """
        # Step 1: Retrieve documents first. This is done separately from the main
        # chain so we can access the full document metadata for creating sources.
        relevant_docs = self.retriever.invoke(question)

        # Handle the edge case where no relevant documents are found.
        if not relevant_docs:
            return {
                "answer": "Unfortunately, I could not find any relevant information "
                          "in my knowledge base.",
                "sources": []
            }

        # Step 2: Prepare the input dictionary for the main chain.
        input_data = {"question": question, "language": language}

        # Step 3: Invoke the main chain to get the final, formatted answer.
        # The chain handles context retrieval, prompting, and LLM generation.
        generated_answer = self.chain.invoke(input_data)

        # Step 4: Format the sources from the retrieved documents.
        sources = self._format_sources(relevant_docs)

        return {"answer": generated_answer, "sources": sources}
