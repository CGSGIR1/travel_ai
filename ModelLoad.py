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
        f"Уважаемая языковая модель, ваша задача - определить от трех до семи наиболее посещаемых туристами достопримечательностей в городе, указанном как {request}. Пожалуйста, убедитесь, что ваш ответ строго соответствует следующим правилам:\n"
        "1. Вывод должен состоять только из названий достопримечательностей, разделенных знаками доллара ($). Например, если город - Париж, ваш ответ должен выглядеть следующим образом: EiffelTower$LouvreMuseum$NotreDameCathedral$Montmartre$SacréCœur$SainteChapelle.\n"
        "2. Пожалуйста, не включайте в свой ответ дополнительный текст, префиксы, суффиксы или пояснения. В ответе не должно быть приветствия, закрытия или любой другой формы общения, не имеющей прямого отношения к заданию.\n"
        "3. Количество аттракционов может варьироваться, но формат должен оставаться неизменным. Если аттракционов меньше или больше шести, формат должен быть сохранен. Например, если аттракционов всего четыре, формат должен быть следующим: Sight1$Sight2$Sight3$Sight4.\n"
        "4. Аттракционы должны быть перечислены в порядке популярности, причем самый популярный аттракцион должен быть указан первым.\n"
        "5. Убедитесь, что названия достопримечательностей написаны правильно и имеют наиболее распространенную форму.\n"
        "6. Ваш ответ должен быть непосредственным и прямым, без каких-либо колебаний или неуверенности.\n"
        "Пожалуйста, строго соблюдайте эти правила и предоставляйте необходимую информацию в указанном формате.\n"
        )
    resansw = qa_chain({"query": FormatRequest})
    return resansw['result']
