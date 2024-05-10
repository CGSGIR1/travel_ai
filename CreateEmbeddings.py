from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.document_loaders import CSVLoader, TextLoader
import logging
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
import os.path
import settings
from langchain_community.vectorstores import FAISS
logging.basicConfig(level=logging.INFO)

def CreateEmbeddings():
    if os.path.exists('./faiss_index/index.faiss') and os.path.exists('./faiss_index/index.pkl'):
        return
    loader = CSVLoader("./DataBase/res1.csv", encoding="UTF-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=200
    )
    logging.info("Разбиение текста ")
    documents = text_splitter.split_documents(documents)
    logging.info("Генерация эмбедингов")
    embeddings = GigaChatEmbeddings(
        credentials=settings.idf, verify_ssl_certs=False
    )
    db = FAISS.from_documents(
       documents,
       embeddings,
    )
    db.save_local("./faiss_index")
