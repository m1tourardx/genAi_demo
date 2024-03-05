import os
import openai
import langchain
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
from dotenv import load_dotenv
import tiktoken

dir_docs = os.path.join(os.getcwd(), 'docs')


class DocumentQueryInput(BaseModel):
    query: str = Field(...,
                       description="It must be equal to the complete input entered by the user.")


class DocumentQuery(BaseTool):
    name = 'document_query'
    description = "This function must be consulted to check information and procedures about the gas dehydration process with TEG. This function should always be consulted. The input to this function must be the complete prompt indicated by the user."
    args_schema: Type[BaseModel] = DocumentQueryInput

    def _run(self,
             query: str,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        def read_pdf(directory_path):
            """
            read_pdf: Função para extrair textos de arquivos PDF
            Utilizamos a função PyPDFDirectoryLoader para apontar para o path indicad e em seguida
            com o file_loader carregamos os arquivos (file_loader.load()).
            Estas são funcionalidades do LangChain.
            """

            file_loader = PyPDFDirectoryLoader(directory_path)
            documents = file_loader.load()

            return documents

        # Aplicando para o path que contém os arquivos de texto de interesse:
        docs = read_pdf(dir_docs)

        # Carregando o token do OpenAI
        load_dotenv(override=True)
        openai_key = os.getenv("OPEN_AI_KEY")

        # Carregando os embeddings do OpenAI
        embeddings_gen = OpenAIEmbeddings(api_key=openai_key)

        # Carregando o banco de dados com os documentos e embeddings
        db = Chroma.from_documents(docs, embeddings_gen)

        # Função para buscar documentos similares
        def similaridades(query, k=2):
            matching_results = db.similarity_search(query, k)
            return matching_results

        llm_case = OpenAI(
            openai_api_key=openai_key, temperature=0.3)
        chain = load_qa_chain(llm_case, chain_type='stuff')

        def response(query):
            search_doc = similaridades(query)
            return chain.run(input_documents=search_doc, question=query)

        return response(query)

    async def _arun(self,
                    query: str,
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")
