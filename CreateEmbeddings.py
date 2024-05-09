from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.document_loaders import CSVLoader, TextLoader
from pickle import dump, load
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
import os.path
import settings

def CreateEmbeddings():

    loader = TextLoader("./DataBase/res1.txt", encoding="UTF-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    documents = text_splitter.split_documents(documents)
    print(f"Total documents: {len(documents)}")

    embeddings_creator = GigaChatEmbeddings(
        credentials=settings.idf, verify_ssl_certs=False
    )
    db = Chroma.from_documents(
       documents,
       embeddings_creator,
       client_settings=Settings(anonymized_telemetry=False),
       persist_directory='./DataBase/db.pkl'
    )
