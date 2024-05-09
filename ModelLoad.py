from pickle import load
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import settings

def GigachatStart():
    with open('./DataBase/documents.pkl', 'rb') as fp:
        documents = load(fp)
    with open('./DataBase/embeddings.pkl', 'rb') as fp:
        embeddings = load(fp)
    llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)

    db = Chroma.from_documents(
       documents,
       embeddings,
       client_settings=Settings(anonymized_telemetry=False),
    )
    #f"Ты являеешься гидом по достопримечательностям России. Тебе нужно найти, 5 самых лучших достопримечательностей в регионе {request}. Ты должен вывести только их адреса, подряд, и разделяя ТОЛЬКО значком '$'"
    return RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    #HumanMessage(content=user_input)

def AIResponse(request, qa_chain):

    FormatRequest = (
        #f" Ты должен вывести ТОЛЬКО полные адреса без пробелов, разделяя ТОЛЬКО значком '$'. Ты являеешься гидом по достопримечательностям России."
                     #f" Тебе нужно найти, 5 самых лучших достопримечательностей в регионе {request}."
                    # f" Достопримечательности Псков: Псковская область, город Псков, ул. Ломоносова, 95$Псковская область, город Псков, проезд Ломоносова, 08$Псковская область, город Псков, пр. Сталина, 96$Псковская область, город Псков, пер. Домодедовская, 42$Псковская область, город Псков, пр. Косиора, 05"
                    # f" Достопримечательности Тюмень: Тюменская область, город Тюмень, спуск Ломоносова, 77$Тюменская область, город Тюмень, ул. Гоголя, 49$Тюменская область, город Тюмень, ул. Ленина, 64$Тюменская область, город Тюмень, ул. 1905 года, 70$Тюменская область, город Тюмень, пр. Ломоносова, 54"
                    # f" Достопримечательности {request}: "
        f"Раскажи какие есть достопримечательности в {request}:"
        )
    resansw = qa_chain({"query": FormatRequest})
    return resansw['result']
