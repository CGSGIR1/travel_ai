from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.document_loaders import CSVLoader, TextLoader
from pickle import dump, load
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
import os.path
import settings



def CreateEmbeddings():
    if os.path.exists('./DataBase/embeddings.pkl') and os.path.exists('./DataBase/documents.pkl'):
        return

    loader = TextLoader("./DataBase/res1.txt", encoding="UTF-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    documents = text_splitter.split_documents(documents)
    print(f"Total documents: {len(documents)}")

    embeddings = GigaChatEmbeddings(
        credentials=settings.idf, verify_ssl_certs=False
    )
    with open('./DataBase/embeddings.pkl', 'wb') as fp:
        dump(embeddings, fp)
    with open('./DataBase/documents.pkl', 'wb') as fp:
        dump(documents, fp)

