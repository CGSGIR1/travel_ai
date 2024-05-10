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
    query = "Коломна"
    llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)
    return db.as_retriever()
    #return RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())


payload = json.dumps({

    "messages": [
        {
            "role": "system",
            "content": "Ты - гид по достопримечательностям. Тебе дан город QUESTION и релевантные достопримечательности из искомого города.\nСоздай краткий и информативный ответ оператора ЦКР, основываясь исключительно на информации из приведённых отрывков.\nОтвечай исходя из имеющейся информации фразой оператора:"
        },
        {
            "role": "user",
            "content": "QUESTION: условия бизнес карты\n========="
                       " Content: Условия по Кредитной бизнес - карте: Лимит от 100 000 до 1 000 000 рублей"
                       " \nСрок 36 месяцев (далее пролонгация автоматом)"
                       " \nНет платы за обслуживание"
                       " \nЛьготный период без процентов – до 120 дней и до 150 у партнёров."
                       " \nСтандартная ставка – 32,4% годовых для с/х; 33,6% - для остальных."
                       " \nПартнеры (http://www.sberbank.ru/ru/s_m_business/cards/credit-businesscards/partners)."
                       " \nБез залога Без поручительства \nОформление от трёх минут \nЛюбые цели \nОплата товаров и услуг в магазинах, на сайтах (нельзя оплачивать через платежные поручения) \nДоступно снятие наличных (комиссия 8%, минимум 300 рублей). Льготный период при снятии сохраняется. \nОбязательный платеж по основному долгу – 5% в месяц от задолженности на дату платежа. Проценты уплачиваются ежемесячно с учетом льготного периода кредитования. Source: /page/a419c30d-f80b-4e37-a9e2-94763bbe7c3a========= Ответ оператора:"

        }
    ],
    "model": "GigaChat-Pro",
    "temperature": 0.01
})
def AIResponse(request, ret, chat):
    chat = GigaChat(credentials=settings.idf, verify_ssl_certs=False)
    docs = ret.invoke(request)
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
