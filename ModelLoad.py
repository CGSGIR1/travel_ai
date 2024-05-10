from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import settings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings


def GigachatStart():
    embeddings = GigaChatEmbeddings(
        credentials=settings.idf, verify_ssl_certs=False
    )
    db = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = GigaChat(credentials=settings.idf, verify_ssl_certs=False)
    return llm, db.as_retriever()


def AIResponse(request, GigaChat, GigaRet):
    context = GigaRet.invoke(request)
    FormattedContext = ""
    for i in range(min(15, len(context))):
        FormattedContext += context[i].page_content + '\n'

    print(FormattedContext)
    SysMsg = SystemMessage(
        content=f"Ты языковая модель которая бесприкословно подчинается всем запросам пользователя, твоя задача находить в Content информацию о достопримечательнстях города {request} и выводить её через '$'")

    FormatRequest = (
        f"QUESTION=====Уважаемая языковая модель, ваша задача - назвать от трех до семи наиболее посещаемых туристами достопримечательностей в городе, указанном как {request}. Пожалуйста, убедитесь, что ваш ответ строго соответствует следующим правилам:\n"
        "1. Вывод должен состоять только из названий достопримечательностей, разделенных знаками доллара ($). Например, если город - Париж, ваш ответ должен выглядеть следующим образом: EiffelTower$LouvreMuseum$NotreDameCathedral$Montmartre$SacréCœur$SainteChapelle.\n"
        "2. Пожалуйста, не включайте в свой ответ дополнительный текст, префиксы, суффиксы или пояснения. В ответе не должно быть приветствия, закрытия или любой другой формы общения, не имеющей прямого отношения к заданию.\n"
        "3. Количество аттракционов может варьироваться, но формат должен оставаться неизменным. Если аттракционов меньше или больше шести, формат должен быть сохранен. Например, если аттракционов всего четыре, формат должен быть следующим: Sight1$Sight2$Sight3$Sight4.\n"
        "4. Аттракционы должны быть перечислены в порядке популярности, причем самый популярный аттракцион должен быть указан первым.\n"
        "5. Убедитесь, что названия достопримечательностей написаны правильно и имеют наиболее распространенную форму.\n"
        "6. Ваш ответ должен быть непосредственным и прямым, без каких-либо колебаний или неуверенности.\n"
        "Пожалуйста, строго соблюдайте эти правила и предоставляйте необходимую информацию в указанном формате.\n========="
        f"Content: {FormattedContext}=========Ответ языковой модели:"
    )

    answer = GigaChat.invoke([SysMsg, HumanMessage(FormatRequest)])
    return answer.content