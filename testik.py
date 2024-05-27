import settings
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import promts


# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=settings.idf, verify_ssl_certs=False)


messages = [
    SystemMessage(
        content=promts.main_gid
    )
]
def GptAnswer(user_input):
    # Ввод пользователя
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    return res.content