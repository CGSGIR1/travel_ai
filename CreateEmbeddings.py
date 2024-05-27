from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.document_loaders import CSVLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import logging
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
import os.path
import settings
from langchain_community.vectorstores import FAISS

logging.basicConfig(level=logging.INFO)

def CreateEmbeddings(file_for_context, model_name ):
    if os.path.exists('./faiss_index/index.faiss') and os.path.exists('./faiss_index/index.pkl'):
        return

    loader = CSVLoader(
        file_for_context,
        encoding="UTF-8",
        source_column='Полный адрес',
        metadata_columns=['Объект', 'На карте', 'Особо ценный объект', 'описание предмета охраны']
                       )

    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=200
    )

    documents = text_splitter.split_documents(raw_documents)
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # создаем хранилище
    db = FAISS.from_documents(documents, embeddings)
    db.as_retriever()

    # также можно сохранить хранилище локально
    db.save_local(settings.FAISS_FOLDER)


CreateEmbeddings(
    file_for_context=os.path.join(settings.ROOT_DIR, "DataBase", "res1.csv"),
    model_name="google-bert/bert-base-uncased"
)

embeddings = HuggingFaceEmbeddings(model_name=settings.emmbedding_model_name)
db = FAISS.load_local(settings.FAISS_FOLDER, embeddings, allow_dangerous_deserialization=True)
