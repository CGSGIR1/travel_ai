from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import settings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
import json

def GigachatStart():
    embeddings = GigaChatEmbeddings(
        credentials=settings.idf, verify_ssl_certs=False
    )
    db = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)
    return RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

def AIResponse(request, chain):

    WeakFormatRequest2 = f"Какие достоприсечательности в {request}?"
    sights = chain({"query": WeakFormatRequest2})

    StrongFormat = (
        f"НЕОБХОДИМО получить достопримечательности из текста: '{sights['result']}' верни их в строго фиксированном формате, разделяя их через знак '$'\n"
        "Должно получиться что-то похожее на 'Достопримечательность 1$Достопримечательность 2$Достопримечательность 3$Достопримечательность 4'\n"
        "НЕ ДОБАВЛЯЙ ЛИШНИХ КОММЕНТАРИЕВ\n"
        f"ЕСЛИ В '{sights['result']}' нет достопримечательностей верни '{request}'"
    )

    answer = chain({"query" : StrongFormat})
    return answer['result']